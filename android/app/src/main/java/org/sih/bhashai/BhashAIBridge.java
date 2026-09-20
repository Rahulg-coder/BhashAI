package org.sih.bhashai;

import android.content.res.AssetFileDescriptor;
import android.media.MediaPlayer;
import android.webkit.JavascriptInterface;
import android.widget.Toast;
import java.io.IOException;

public class BhashAIBridge {

    private final MainActivity activity;
    private MediaPlayer mediaPlayer;

    public BhashAIBridge(MainActivity activity) {
        this.activity = activity;
    }

    @JavascriptInterface
    public void startListening() {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.startNativeSpeechRecognition(false);
            }
        });
    }

    @JavascriptInterface
    public void stopListening() {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.stopNativeSpeechRecognition();
            }
        });
    }

    @JavascriptInterface
    public void startContinuousListening() {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.startContinuousClassroomRecognition();
            }
        });
    }

    @JavascriptInterface
    public void stopContinuousListening() {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.stopNativeSpeechRecognition();
            }
        });
    }

    @JavascriptInterface
    public void playSantaliAudio(final String filename) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                playAssetAudio("audio/" + filename);
            }
        });
    }

    @JavascriptInterface
    public void speakHindi(final String text) {
        activity.speakHindi(text);
    }

    @JavascriptInterface
    public void speakSantali(final String phoneticText, final String audioFileName) {
        activity.speakSantaliDeva(phoneticText, audioFileName);
    }

    @JavascriptInterface
    public void speakSantaliDeva(final String devaPhonetic, final String audioFileName) {
        activity.speakSantaliDeva(devaPhonetic, audioFileName);
    }

    @JavascriptInterface
    public void setSpeechRate(final float rate) {
        activity.setSpeechRate(rate);
    }

    @JavascriptInterface
    public void vibrate(final int ms) {
        activity.vibrate(ms);
    }

    @JavascriptInterface
    public void showToast(final String message) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                Toast.makeText(activity, message, Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void playAssetAudio(final String assetPath) {
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                AssetFileDescriptor afd = null;
                try {
                    if (mediaPlayer != null) {
                        try {
                            mediaPlayer.stop();
                            mediaPlayer.reset();
                            mediaPlayer.release();
                        } catch (Exception ignored) {}
                        mediaPlayer = null;
                    }

                    mediaPlayer = new MediaPlayer();
                    try {
                        afd = activity.getAssets().openFd(assetPath);
                    } catch (IOException e) {
                        // Fallback to default santali audio if specific asset not found
                        afd = activity.getAssets().openFd("audio/default_santali.mp3");
                    }

                    mediaPlayer.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
                    mediaPlayer.prepare();
                    mediaPlayer.start();
                    afd.close();
                } catch (Exception e) {
                    e.printStackTrace();
                    if (afd != null) {
                        try { afd.close(); } catch (Exception ignored) {}
                    }
                }
            }
        });
    }

    public void release() {
        if (mediaPlayer != null) {
            try {
                mediaPlayer.release();
            } catch (Exception ignored) {}
            mediaPlayer = null;
        }
    }
}
