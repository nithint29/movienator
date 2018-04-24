package com.example.admin.movienator;

import android.os.SystemClock;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

public class PastMovies extends AppCompatActivity {
    public static String resp;
    String[] images = {"https://ia.media-imdb.com/images/M/MV5BMTk2NTI1MTU4N15BMl5BanBnXkFtZTcwODg0OTY0Nw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "https://ia.media-imdb.com/images/M/MV5BMjAzNzk5MzgyNF5BMl5BanBnXkFtZTcwOTE4NDU5Ng@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "https://ia.media-imdb.com/images/M/MV5BNTg2OTY2ODg5OF5BMl5BanBnXkFtZTcwODM5MTYxOA@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "https://ia.media-imdb.com/images/M/MV5BZDEyN2NhMjgtMjdhNi00MmNlLWE5YTgtZGE4MzNjMTRlMGEwXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "https://ia.media-imdb.com/images/M/MV5BNzMxNTExOTkyMF5BMl5BanBnXkFtZTcwMzEyNDc0OA@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "https://ia.media-imdb.com/images/M/MV5BMTY5NzY5NTY2NF5BMl5BanBnXkFtZTcwNTg3NzIxNA@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "https://ia.media-imdb.com/images/M/MV5BMTM5OTMyMjIxOV5BMl5BanBnXkFtZTcwNzU4MjIwNQ@@._V1_UX182_CR0,0,182,268_AL_.jpg"};



    String[] title = {"Avengers", "Hugo","Life of Pi", "Spider-Man", "Wreck-It Ralph","Another Year", "The Help"};

    String[] prediction = {"5.1", "2.2", "1.7", "3.7", "2.5", "1.2", "1.5"};

    ListView lView;

    ListAdapter lAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_past_movies);

//        RequestQueue queue = Volley.newRequestQueue(this);
//        String url ="http://172.30.20.201:5000/info";
//
//// Request a string response from the provided URL.
//        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
//                new Response.Listener<String>() {
//                    @Override
//                    public void onResponse(String response) {
//                        // Display the first 500 characters of the response string.
////                        mTextView.setText("Response is: "+ response.substring(0,500));
//                        PastMovies.resp = response;
//                        Toast.makeText(getApplicationContext(), response.substring(0,500), Toast.LENGTH_SHORT).show();
//                    }
//                }, new Response.ErrorListener() {
//            @Override
//            public void onErrorResponse(VolleyError error) {
//                Toast.makeText(getApplicationContext(), "bitch", Toast.LENGTH_SHORT).show();
////                mTextView.setText("That didn't work!");
//            }
//        });
//
//        queue.add(stringRequest);


        JSONObject j;
        JSONArray jarr;
//        SystemClock.sleep(3000);
        try{
            jarr = new JSONArray(resp);
//            jarr = j.getJSONArray(resp);
            Toast.makeText(getApplicationContext(), ""+ jarr.length(), Toast.LENGTH_SHORT).show();

            int size = jarr.length();
            title = new String[size];
            images = new String[size];
            prediction = new String[size];
            for(int i=0;i<size;i++){
                title[i] = jarr.getJSONObject(i).get("title").toString();
                images[i] = "http://image.tmdb.org/t/p/w185/"+jarr.getJSONObject(i).get("poster_path").toString();
                prediction[i] = jarr.getJSONObject(i).get("revenue").toString();
            }
        }
        catch(Exception e){
            e.printStackTrace();
            Toast.makeText(getApplicationContext(), "error", Toast.LENGTH_SHORT).show();
        }





        lView = (ListView) findViewById(R.id.androidList);

        lAdapter = new ListAdapter(PastMovies.this, title, prediction, images);

        lView.setAdapter(lAdapter);

        lView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

                Toast.makeText(PastMovies.this, title[i]+" "+prediction[i], Toast.LENGTH_SHORT).show();

            }
        });

    }
}
