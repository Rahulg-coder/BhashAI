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
    public void stopAudio() {
        activity.stopAllAudio();
    }

    @JavascriptInterface
    public void playSantaliAudio(final String filename) {
        playAssetAudio("audio/" + filename);
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

    public boolean playAssetAudioIfExists(final String assetPath) {
        AssetFileDescriptor afd = null;
        try {
            afd = activity.getAssets().openFd(assetPath);
        } catch (IOException e) {
            return false;
        }

        final AssetFileDescriptor finalAfd = afd;
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    stopMediaPlayer();
                    activity.stopTTS();
                    activity.setAudioPlaying(true);

                    mediaPlayer = new MediaPlayer();
                    mediaPlayer.setDataSource(finalAfd.getFileDescriptor(), finalAfd.getStartOffset(), finalAfd.getLength());
                    mediaPlayer.prepare();
                    mediaPlayer.start();
                    mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                        @Override
                        public void onCompletion(MediaPlayer mp) {
                            stopMediaPlayer();
                            activity.setAudioPlaying(false);
                            activity.onPlaybackFinished();
                        }
                    });
                    mediaPlayer.setOnErrorListener(new MediaPlayer.OnErrorListener() {
                        @Override
                        public boolean onError(MediaPlayer mp, int what, int extra) {
                            stopMediaPlayer();
                            activity.setAudioPlaying(false);
                            activity.onPlaybackFinished();
                            return true;
                        }
                    });
                    finalAfd.close();
                } catch (Exception e) {
                    e.printStackTrace();
                    stopMediaPlayer();
                    activity.setAudioPlaying(false);
                    try { finalAfd.close(); } catch (Exception ignored) {}
                }
            }
        });
        return true;
    }

    public void playAssetAudio(final String assetPath) {
        boolean played = playAssetAudioIfExists(assetPath);
        if (!played) {
            stopMediaPlayer();
            activity.setAudioPlaying(false);
        }
    }

    public void stopMediaPlayer() {
        if (mediaPlayer != null) {
            try {
                if (mediaPlayer.isPlaying()) {
                    mediaPlayer.stop();
                }
                mediaPlayer.reset();
                mediaPlayer.release();
            } catch (Exception ignored) {}
            mediaPlayer = null;
        }
    }

    public void release() {
        stopMediaPlayer();
    }
}
