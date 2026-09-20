package org.sih.bhashai;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Vibrator;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import java.util.ArrayList;
import java.util.Locale;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_REQUEST_RECORD_AUDIO = 201;

    private WebView webView;
    private SpeechRecognizer speechRecognizer;
    private BhashAIBridge bridge;
    private TextToSpeech textToSpeech;
    private boolean ttsReady = false;

    private float speechRate = 0.88f;
    private float speechPitch = 1.0f;

    private boolean isListening = false;
    private boolean isContinuousMode = false;
    private final Handler mainHandler = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        // Hardware-accelerated WebView
        webView = new WebView(this);
        setContentView(webView);

        bridge = new BhashAIBridge(this);
        configureWebView();
        initTTS();
        checkPermissions();

        // Load 100% Offline Local Assets
        webView.loadUrl("file:///android_asset/index.html");
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                MainActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        request.grant(request.getResources());
                    }
                });
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return false;
            }
        });

        // Register Java interface bridge
        webView.addJavascriptInterface(bridge, "BhashAIBridge");
    }

    private void initTTS() {
        textToSpeech = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    ttsReady = true;
                    int result = textToSpeech.setLanguage(new Locale("hi", "IN"));
                    if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        textToSpeech.setLanguage(Locale.getDefault());
                    }
                }
            }
        });
    }

    public void setSpeechRate(float rate) {
        this.speechRate = Math.max(0.5f, Math.min(2.0f, rate));
    }

    public void setSpeechPitch(float pitch) {
        this.speechPitch = Math.max(0.5f, Math.min(2.0f, pitch));
    }

    public void speakHindi(final String text) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (textToSpeech != null && ttsReady) {
                    textToSpeech.stop();
                    textToSpeech.setLanguage(new Locale("hi", "IN"));
                    textToSpeech.setPitch(speechPitch);
                    textToSpeech.setSpeechRate(speechRate);
                    textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, "hindi_tts");
                } else {
                    Toast.makeText(MainActivity.this, "Hindi TTS initializing...", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    public void speakSantaliDeva(final String devaPhonetic, final String audioFileName) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String targetFile = audioFileName;
                if (targetFile == null || targetFile.trim().isEmpty() ||
                    targetFile.equals("null") || targetFile.equals("undefined")) {
                    targetFile = "default_santali.mp3";
                }
                bridge.playAssetAudio("audio/" + targetFile);
            }
        });
    }

    public void stopTTS() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (textToSpeech != null) {
                    textToSpeech.stop();
                }
            }
        });
    }

    public void vibrate(int ms) {
        try {
            Vibrator v = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
            if (v != null && v.hasVibrator()) {
                v.vibrate(ms);
            }
        } catch (Exception ignored) {}
    }

    private void checkPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                    this,
                    new String[]{Manifest.permission.RECORD_AUDIO},
                    PERMISSION_REQUEST_RECORD_AUDIO
            );
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_RECORD_AUDIO) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Microphone enabled for BhashAI", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "Microphone permission is required for Hindi speech translation", Toast.LENGTH_LONG).show();
            }
        }
    }

    public void startNativeSpeechRecognition() {
        startNativeSpeechRecognition(false);
    }

    public void startContinuousClassroomRecognition() {
        startNativeSpeechRecognition(true);
    }

    public void startNativeSpeechRecognition(final boolean continuous) {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            Toast.makeText(this, "Speech recognition engine not found on device", Toast.LENGTH_SHORT).show();
            return;
        }

        isContinuousMode = continuous;

        if (speechRecognizer != null) {
            try {
                speechRecognizer.cancel();
                speechRecognizer.destroy();
            } catch (Exception ignored) {}
            speechRecognizer = null;
        }

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        final Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN");
        intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true);

        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle params) {
                isListening = true;
            }

            @Override
            public void onBeginningOfSpeech() {}

            @Override
            public void onRmsChanged(float rmsdB) {
                if (rmsdB > 0.5f) {
                    final float normalized = Math.min(1.0f, Math.max(0.1f, (rmsdB + 2.0f) / 10.0f));
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            webView.evaluateJavascript("javascript:if(window.onMicRmsChanged) window.onMicRmsChanged(" + normalized + ");", null);
                        }
                    });
                }
            }

            @Override
            public void onBufferReceived(byte[] buffer) {}

            @Override
            public void onEndOfSpeech() {
                isListening = false;
            }

            @Override
            public void onError(int error) {
                isListening = false;
                if (isContinuousMode) {
                    if (error == SpeechRecognizer.ERROR_SPEECH_TIMEOUT ||
                        error == SpeechRecognizer.ERROR_NO_MATCH ||
                        error == SpeechRecognizer.ERROR_RECOGNIZER_BUSY) {
                        mainHandler.postDelayed(new Runnable() {
                            @Override
                            public void run() {
                                if (isContinuousMode) {
                                    startNativeSpeechRecognition(true);
                                }
                            }
                        }, 250);
                        return;
                    }
                }

                final String msg = getErrorMessage(error);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        webView.evaluateJavascript("if(window.onNativeSpeechError) window.onNativeSpeechError(" + JSONObject.quote(msg) + ");", null);
                    }
                });
            }

            @Override
            public void onResults(Bundle results) {
                isListening = false;
                ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if (matches != null && !matches.isEmpty()) {
                    final String text = matches.get(0);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            if (isContinuousMode) {
                                webView.evaluateJavascript("if(window.onContinuousFinal) window.onContinuousFinal(" + JSONObject.quote(text) + ");", null);
                            } else {
                                webView.evaluateJavascript("if(window.onNativeSpeechFinal) window.onNativeSpeechFinal(" + JSONObject.quote(text) + ");", null);
                            }
                        }
                    });
                }

                if (isContinuousMode) {
                    mainHandler.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            if (isContinuousMode) {
                                startNativeSpeechRecognition(true);
                            }
                        }
                    }, 200);
                }
            }

            @Override
            public void onPartialResults(Bundle partialResults) {
                ArrayList<String> matches = partialResults.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if (matches != null && !matches.isEmpty()) {
                    final String partial = matches.get(0);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            if (isContinuousMode) {
                                webView.evaluateJavascript("if(window.onContinuousPartial) window.onContinuousPartial(" + JSONObject.quote(partial) + ");", null);
                            } else {
                                webView.evaluateJavascript("if(window.onNativeSpeechPartial) window.onNativeSpeechPartial(" + JSONObject.quote(partial) + ");", null);
                            }
                        }
                    });
                }
            }

            @Override
            public void onEvent(int eventType, Bundle params) {}
        });

        speechRecognizer.startListening(intent);
    }

    public void stopNativeSpeechRecognition() {
        isContinuousMode = false;
        if (speechRecognizer != null) {
            try {
                speechRecognizer.stopListening();
                speechRecognizer.cancel();
            } catch (Exception ignored) {}
            isListening = false;
        }
    }

    private String getErrorMessage(int errorCode) {
        switch (errorCode) {
            case SpeechRecognizer.ERROR_AUDIO: return "Audio recording error";
            case SpeechRecognizer.ERROR_CLIENT: return "Client error";
            case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS: return "Insufficient permissions";
            case SpeechRecognizer.ERROR_NETWORK: return "Network error (offline speech recommended in device settings)";
            case SpeechRecognizer.ERROR_NO_MATCH: return "No speech recognized";
            case SpeechRecognizer.ERROR_RECOGNIZER_BUSY: return "Recognizer busy";
            case SpeechRecognizer.ERROR_SERVER: return "Server error";
            case SpeechRecognizer.ERROR_SPEECH_TIMEOUT: return "No speech input";
            default: return "Speech recognition error: " + errorCode;
        }
    }

    @Override
    protected void onDestroy() {
        if (speechRecognizer != null) {
            try {
                speechRecognizer.destroy();
            } catch (Exception ignored) {}
            speechRecognizer = null;
        }
        if (textToSpeech != null) {
            try {
                textToSpeech.stop();
                textToSpeech.shutdown();
            } catch (Exception ignored) {}
            textToSpeech = null;
        }
        if (bridge != null) {
            bridge.release();
        }
        super.onDestroy();
    }
}
