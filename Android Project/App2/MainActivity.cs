using Android.App;

using Android.OS;
using System.Net.Http;

using Android.Widget;
using System;
using System.Collections.Generic;
using Android.Content;
using Android.Preferences;
using Newtonsoft.Json.Linq;
using System.Text;

namespace App2

{

    [Activity(Label = "Smart Outdoor Workout", MainLauncher = true)]

    public class MainActivity : Activity

    {

        EditText txtUserName, txtPassWord;
        private static readonly HttpClient client = new HttpClient();


        protected override void OnCreate(Bundle bundle)

        {

            base.OnCreate(bundle);
            // Set our view from the "main" layout resource

            SetContentView(Resource.Layout.activity_main);


            txtUserName = FindViewById<EditText>(Resource.Id.txtUserName);

            txtPassWord = FindViewById<EditText>(Resource.Id.txtPassword);

            Button loginBtn = FindViewById<Button>(Resource.Id.loginBtn);
            Button signupBtn = FindViewById<Button>(Resource.Id.signupBtn);

            loginBtn.Click += OnLogin;
            signupBtn.Click += OnSignup;
            Context mContext = Application.Context;
            ISharedPreferences prefs = PreferenceManager.GetDefaultSharedPreferences(mContext);
            ISharedPreferencesEditor editor = prefs.Edit();
            editor.Remove("username");
            editor.Remove("machine");
            editor.Apply();        // applies changes asynchronously on newer APIs

        }

        public override void OnBackPressed()
        {
        }

        async void OnLogin(object sender, EventArgs e)

        {

            string sUserName = txtUserName.Text;

            string sPassword = txtPassWord.Text;

            string sContentType = "application/json"; // or application/xml

            JObject oJsonObject = new JObject();
            oJsonObject.Add("username", sUserName);
            oJsonObject.Add("password", sPassword);
            var response = await client.PostAsync("http://40.113.134.7/APP/signin/", new StringContent(oJsonObject.ToString(), Encoding.UTF8, sContentType));
            var res = await response.Content.ReadAsStringAsync();
            if (res.ToString().Equals("User Found"))
                {
                    Context mContext = Application.Context;
                    ISharedPreferences prefs = PreferenceManager.GetDefaultSharedPreferences(mContext);
                    ISharedPreferencesEditor editor = prefs.Edit();
                    editor.PutString("username", sUserName);
                    editor.Apply();        // applies changes asynchronously on newer APIs
                    StartActivity(typeof(UserActivity));
                }
                else// bad user or pass 
                {
                    AlertDialog.Builder alert = new AlertDialog.Builder(this);
                    alert.SetTitle("FAILURE");
                    //alert.SetMessage("Wrong username or password.");
                    alert.SetMessage(response.ToString());
                    alert.SetPositiveButton("Try again", (senderAlert, args) =>
                    {
                    });
                    Dialog dialog = alert.Create();
                    dialog.Show();
                }
        }

        void OnSignup(object sender, EventArgs e)

        {
            StartActivity(typeof(SignUpActivity));
        }

    }

}