package com.example.jurin;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class TrendViewAdapter extends RecyclerView.Adapter<TrendViewAdapter.Holder> {
    private Context context;
    private List<trendItem> list = new ArrayList<>();

    public TrendViewAdapter(Context context,List<trendItem> list) {
        this.context = context;
        this.list = list;
    }

    @NonNull
    @Override
    public TrendViewAdapter.Holder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.trend_item, parent, false);
        Holder holder = new Holder(view);
        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull TrendViewAdapter.Holder holder, int position) {
        int itemposition = position;
        holder.trendNumber.setImageResource(context.getResources().getIdentifier("key_"+String.valueOf(list.get(itemposition).trendNumber),"drawable",context.getPackageName()));
        holder.trendName.setText(list.get(itemposition).trendName);
    }

    @Override
    public int getItemCount() {
        return list.size();
    }
    // ViewHolder는 하나의 View를 보존하는 역할을 한다
    public class Holder extends RecyclerView.ViewHolder{
        public ImageView trendNumber;
        public TextView trendName;

        public Holder(View view){
            super(view);
            trendNumber = (ImageView) view.findViewById(R.id.trendnumber);
            trendName = (TextView) view.findViewById(R.id.trendname);
        }
    }

}
