package org.naija.hasher;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;

import java.io.FileInputStream;
import java.io.InputStream;
import java.security.MessageDigest;

/**
 * Exported activity: takes the URI from the launching Intent's data field,
 * reads that file (either a plain file:// path or via ContentResolver for
 * content:// URIs) and returns its SHA-256 hex digest as the "hash" result
 * extra. Any caller that can start this activity for result gets to hash an
 * arbitrary file it can point a URI at - no permission check is done on the
 * URI itself.
 */
public class HashActivity extends Activity {
    private static final String TAG = "HashActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent result = new Intent();
        try {
            Uri uri = getIntent().getData();
            result.putExtra("hash", calcHash(uri));
            setResult(Activity.RESULT_OK, result);
        } catch (Exception e) {
            Log.e(TAG, "hashing failed", e);
            setResult(Activity.RESULT_CANCELED, result);
        }
        finish();
    }

    // SHA-256 over the file's bytes, streamed in 8KB chunks; returned as lowercase hex.
    private String calcHash(Uri uri) throws Exception {
        InputStream in;
        if ("file".equals(uri.getScheme()) || uri.getScheme() == null) {
            in = new FileInputStream(uri.getPath());
        } else {
            in = getContentResolver().openInputStream(uri);
        }
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        try {
            byte[] buf = new byte[8192];
            int n;
            while ((n = in.read(buf)) > 0) {
                md.update(buf, 0, n);
            }
        } finally {
            in.close();
        }
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
