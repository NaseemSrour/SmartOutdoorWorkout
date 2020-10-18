using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;

using Android.App;
using Android.Content;
using Android.Graphics;
using Android.OS;
using Android.Preferences;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System.Timers;

using static Android.Views.View;

namespace App2
{
    [Activity(Label = "Your Session Overview")]
    public class ImageVis : Activity
    {
        TextView repeatsTxt, setsTxt, timeTxt, caloriesTxt;
        ImageView accImg, speedImg;
        Context mContext;
        ISharedPreferences prefs;
        private static readonly HttpClient client = new HttpClient();
        string acc_url, speed_url;

        protected override void OnCreate(Bundle savedInstanceState)
        {

            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.imageVis);
            mContext = Application.Context;
            prefs = PreferenceManager.GetDefaultSharedPreferences(mContext);
            accImg = FindViewById<ImageView>(Resource.Id.accImg);
            speedImg = FindViewById<ImageView>(Resource.Id.speedImg);
            repeatsTxt = FindViewById<TextView>(Resource.Id.repsTxt);
            setsTxt = FindViewById<TextView>(Resource.Id.setsTxt);
            timeTxt = FindViewById<TextView>(Resource.Id.timeTxt);
            caloriesTxt = FindViewById<TextView>(Resource.Id.caloriesTxt);

                RunOnUiThread(async () => {
                    string temp = await GetRespAsStringLastSessionAsync("numberofrepeats");
                    int checkIfInt;
                    double checkIfDouble;
                    if (!Int32.TryParse(temp,out checkIfInt))
                        repeatsTxt.Text = "0";
                    else
                        repeatsTxt.Text = temp;
                    temp = await GetRespAsStringLastSessionAsync("numberofsets");
                    if (!Int32.TryParse(temp, out checkIfInt))
                        setsTxt.Text = "0";
                    else
                        setsTxt.Text = temp;
                    temp = await GetRespAsStringLastSessionAsync("sessiontime");
                    if (!Double.TryParse(temp, out checkIfDouble))
                        timeTxt.Text = "0";
                    else
                        timeTxt.Text = (Math.Round(checkIfDouble / 60.0, 2)).ToString() + " mins";
                    temp = await GetRespAsStringLastSessionAsync("calories");
                    if (!Int32.TryParse(temp, out checkIfInt))
                        caloriesTxt.Text = "0";
                    else
                        caloriesTxt.Text = temp;
                });
            // Create your application here
            if (prefs.GetString("prevActivity", "").Equals("UserActivity"))
            {
                acc_url = "http://40.113.134.7/APP/Visualise/usersession/acc/overview/?username=" + prefs.GetString("username","");
                speed_url = "http://40.113.134.7/APP/Visualise/usersession/speed/overview/?username=" + prefs.GetString("username", "");
            }
            else // History
            {
                acc_url = "http://40.113.134.7/APP/Visualise/usersession/acc/overview/?username=" + prefs.GetString("username", "") + "&sessionID="+ prefs.GetString("sessionID","");
                speed_url = "http://40.113.134.7/APP/Visualise/usersession/speed/overview/?username=" + prefs.GetString("username", "") + "&sessionID=" + prefs.GetString("sessionID", "");
            }

            if (!acc_url.Equals("0") && !speed_url.Equals("0"))
            {
                Bitmap accBitmap = GetImageBitmapFromUrl(acc_url), speedBitmap = GetImageBitmapFromUrl(speed_url);
                accImg.SetImageBitmap(accBitmap);
                speedImg.SetImageBitmap(speedBitmap);
            }
        }

        private async System.Threading.Tasks.Task<string> GetRespAsStringLastSessionAsync(string methodName)
        {
            var response = await client.GetAsync("http://40.113.134.7/APP/Visualise/usersession/" + methodName + "/?username=" + prefs.GetString("username", ""));
            var res = await response.Content.ReadAsStringAsync();
            return res;
        }
        private async System.Threading.Tasks.Task<string> GetRespAsStringSomeSessionAsyncs(string methodName)
        {
            var response = await client.GetAsync("http://40.113.134.7/APP/Visualise/usersession/" + methodName + "/?username=" + prefs.GetString("username", "") + "&sessionID=" + prefs.GetString("sessionID",""));
            var res = await response.Content.ReadAsStringAsync();
            return res;
        }
        private Bitmap GetImageBitmapFromUrl(string url)
        {
            Bitmap imageBitmap = null;

            using (var webClient = new System.Net.WebClient())
            {
                var imageBytes = webClient.DownloadData(url);
                if (imageBytes != null && imageBytes.Length > 0)
                {
                    imageBitmap = BitmapFactory.DecodeByteArray(imageBytes, 0, imageBytes.Length);
                }
            }

            return imageBitmap;
        }
    }
}