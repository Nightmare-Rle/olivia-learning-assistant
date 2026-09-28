package com.nrle.olivia;

import android.app.Activity;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.Window;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (Build.VERSION.SDK_INT >= 21) {
            Window w = getWindow();
            w.setStatusBarColor(Color.parseColor("#2C3E50"));
            try {
                w.setNavigationBarColor(Color.parseColor("#FFFFFF"));
            } catch (Throwable ignored) {}
        }
        web = new WebView(this);
        configureWebView();
        setContentView(web);
        web.loadUrl("file:///android_asset/www/index.html");
    }

    private void configureWebView() {
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        if (Build.VERSION.SDK_INT >= 21) {
            s.setAllowFileAccessFromFileURLs(true);
            s.setAllowUniversalAccessFromFileURLs(true);
        }
        s.setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
        s.setSupportZoom(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        web.setWebViewClient(new WebViewClient());
        web.setBackgroundColor(Color.parseColor("#EAF2F8"));
        web.setOverScrollMode(WebView.OVER_SCROLL_NEVER);
        if (Build.VERSION.SDK_INT >= 23) {
            s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (web != null) web.onPause();
    }

    @Override
    protected void onDestroy() {
        if (web != null) {
            web.stopLoading();
            web.setWebChromeClient(null);
            web.setWebViewClient(null);
            web.destroy();
            web = null;
        }
        super.onDestroy();
    }
}