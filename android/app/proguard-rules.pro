# BhashAI ProGuard Rules for 2GB RAM device optimization
-keepattributes JavascriptInterface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class org.sih.bhashai.** { *; }
