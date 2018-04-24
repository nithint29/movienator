package com.example.admin.movienator;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

public class PastMovies extends AppCompatActivity {

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
