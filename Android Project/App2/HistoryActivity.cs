using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;

using Android.App;
using Android.Content;
using Android.OS;
using Android.Preferences;
using Android.Runtime;
using Android.Views;
using Android.Widget;

namespace App2
{
    [Activity(Label = "My Workout Sessions")]
    public class HistoryActivity : Activity
    {
        List<Session> sessionsList;
        SessionAdapter adapter;
        ListView sessionsListView;

        private static readonly HttpClient client = new HttpClient();
        Context mContext;
        ISharedPreferences prefs;
        ISharedPreferencesEditor editor;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.history_activity);

            mContext = Application.Context;
            prefs = PreferenceManager.GetDefaultSharedPreferences(mContext);
            editor = prefs.Edit();
            sessionsListView = FindViewById<ListView>(Resource.Id.sessionsList);
            string res = null;
            List<Session> tmpSessionsList = new List<Session>();

            this.RunOnUiThread(async () =>
            {
                var response = await client.GetAsync("http://40.113.134.7/APP/UserHistory/?username=" + prefs.GetString("username", ""));
                res = await response.Content.ReadAsStringAsync();
                if (res != null && !res.Equals("None"))
                {
                    string[] sessions = res.Split('\n');
                    foreach (string session in sessions)
                    {
                        string id = session.Split(' ')[0];
                        if (id.Length <= 1)
                            break;
                        int descStartLen = session.Split(' ')[0].Length;
                        descStartLen += 2;
                        tmpSessionsList.Add(new Session() { Id = id, Description = session.Substring(descStartLen) });
                    }
                }
            });
            sessionsList = new List<Session>();
            Handler h = new Handler();
            Action delayedAction = () =>
            {
                sessionsList = tmpSessionsList;
                adapter = new SessionAdapter(this, sessionsList);
                sessionsListView.Adapter = adapter;
                sessionsListView.ItemClick += SessionsListView_ItemClick;
            };

            h.PostDelayed(delayedAction, 2000);
            
            
        }
        private void SessionsListView_ItemClick(object sender, AdapterView.ItemClickEventArgs e)
        {
            var sessionID = sessionsList[e.Position].Id;
            editor.PutString("sessionID", sessionID);
            editor.PutString("prevActivity", "HistoryActivity");
            editor.Apply();
            
            StartActivity(typeof(ImageVis));
        }
    }
}