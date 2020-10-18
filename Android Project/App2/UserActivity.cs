using System;
using Android.App;
using Android.Content;

using Android.OS;
using Android.Preferences;
using System.Data;
using MySql.Data.MySqlClient;
using Android.Widget;

using Android.Content.PM;

using ZXing.Mobile;
using System.Collections.Generic;
using System.Net.Http;
using Newtonsoft.Json.Linq;
using System.Text;
using System.Timers;
using Android.Graphics;

namespace App2
{
    [Activity(Label = "Smart Outdoor Workout", ConfigurationChanges=ConfigChanges.Orientation|ConfigChanges.KeyboardHidden)]
    public class UserActivity : Activity
    { 
        TextView helloUser;
        TextView timerTxt, setsTxt, repsTxt, totalRepsTxt;
        Button startTrainingBtn;
        Button stopTrainingBtn, historyBtn, logoutBtn;
        String user, machine;
        int mins = 0, secs = 0, millisecond = 1;
        int totalReps = 0;
        int repsNotChangedCounter = 0;
        int lastTotalReps = 0;
        int setsNum = 0;
        Timer timer, repsTimer;
        MobileBarcodeScanner scanner;
        private static readonly HttpClient client = new HttpClient();
        Context mContext;
        ISharedPreferences prefs;
        ISharedPreferencesEditor editor;
        GridLayout gridLayout;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.user_activity);
            helloUser = FindViewById<TextView>(Resource.Id.txtHello);
            timerTxt = FindViewById<TextView>(Resource.Id.txtTimer);
            setsTxt = FindViewById<TextView>(Resource.Id.txtSets);
            repsTxt = FindViewById<TextView>(Resource.Id.txtRepsSet);
            totalRepsTxt = FindViewById<TextView>(Resource.Id.txtTotalReps);
            gridLayout = FindViewById<GridLayout>(Resource.Id.gridLayout2);
            mContext = Application.Context;
            prefs = PreferenceManager.GetDefaultSharedPreferences(mContext);
            editor = prefs.Edit();

            timer = null;
            repsTimer = null;
            timer = new Timer();
            timer.Interval = 1; // 1 Milliseconds  
            timer.Elapsed += Timer_Elapsed;
            repsTimer = new Timer();
            repsTimer.Interval = 500; 
            repsTimer.Elapsed += RepsTimer_ElapsedAsync;

            user = prefs.GetString("username", "");
            helloUser.SetText(("Hello " + user + "!").ToCharArray(), 0, user.Length + 7);
            logoutBtn = FindViewById<Button>(Resource.Id.logoutBtn);
            startTrainingBtn = FindViewById<Button>(Resource.Id.startTrainingBtn);
            stopTrainingBtn = FindViewById<Button>(Resource.Id.stopTrainingBtn);
            historyBtn = FindViewById<Button>(Resource.Id.historyBtn);

            machine = prefs.GetString("machine", "");
            if (!machine.Equals("")) // already on machine
            {
                helloUser.SetText(("Hello " + user + "! You are working on machine " + machine).ToCharArray(), 0, user.Length + 6 + machine.Length + "! You are working on machine ".Length);
                startTrainingBtn.Visibility = Android.Views.ViewStates.Gone;
                stopTrainingBtn.Visibility = Android.Views.ViewStates.Visible;
                gridLayout.Visibility = Android.Views.ViewStates.Visible;
            }
            else
            {
                helloUser.SetText(("Hello " + user + "!").ToCharArray(), 0, user.Length + 6 );
                startTrainingBtn.Visibility = Android.Views.ViewStates.Visible;
                stopTrainingBtn.Visibility = Android.Views.ViewStates.Gone;
                gridLayout.Visibility = Android.Views.ViewStates.Gone;
            }
            MobileBarcodeScanner.Initialize(Application);
            scanner = new MobileBarcodeScanner();

            logoutBtn.Click += OnLogout;
            startTrainingBtn.Click += OnStartTraining;
            stopTrainingBtn.Click += OnStopTraining;
            historyBtn.Click += OnHistory;

            // Create your application here
        }
        void OnHistory(object sender, EventArgs e)
        {

            StartActivity(typeof(HistoryActivity));

            // Do something with someValue
            //    }
        }
        void OnLogout(object sender, EventArgs e)
        {
            AlertDialog.Builder alert = new AlertDialog.Builder(this);
            alert.SetTitle("Logout?");
            alert.SetMessage("Are you sure you want to log out?");
            alert.SetPositiveButton("YES", async delegate
            {
                editor.Remove("username");
                editor.Remove("machine");
                editor.Remove("prevActivity");
                editor.Apply();        // applies changes asynchronously on newer APIs
                base.OnBackPressed();
            });
            alert.SetNegativeButton("Cancel", (senderAlert, args) =>
            {
            });
            Dialog dialog = alert.Create();
            dialog.Show();
        }
        protected override void OnResume()
        {
            base.OnResume();

            if (ZXing.Net.Mobile.Android.PermissionsHandler.NeedsPermissionRequest(this))
                ZXing.Net.Mobile.Android.PermissionsHandler.RequestPermissionsAsync(this);
        }
        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, Permission[] grantResults)
        {
            global::ZXing.Net.Mobile.Android.PermissionsHandler.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
        public override void OnBackPressed()
        {
            
        }
        void OnStartTraining(object sender, EventArgs e)
        {
            mins = 0;
            secs = 0;
            millisecond = 1;
            totalReps = 0;
            repsNotChangedCounter = 0;
            lastTotalReps = 0;
            setsNum = 0;
            timer = null;
            repsTimer = null;
            timer = new Timer();
            timer.Interval = 1; // 1 Milliseconds  
            timer.Elapsed += Timer_Elapsed;
            repsTimer = new Timer();
            repsTimer.Interval = 500;
            repsTimer.Elapsed += RepsTimer_ElapsedAsync;
            AlertDialog.Builder alert = new AlertDialog.Builder(this);
            alert.SetTitle("Start training");
            alert.SetMessage("Please scan the barcode on the machine you wish to train on.");
            alert.SetPositiveButton("OK", async delegate
            {
                scanner.UseCustomOverlay = false;

                    //We can customize the top and bottom text of the default overlay
                    scanner.TopText = "Hold the camera up to the barcode\nAbout 6 inches away";
                scanner.BottomText = "Wait for the barcode to automatically scan!";

                    //Start scanning
                    var result = await scanner.Scan();
                if (result != null && !string.IsNullOrEmpty(result.Text))
                {
                        /*msg = "Found Barcode: " + result.Text;
                        this.RunOnUiThread(() => {
                            Toast.MakeText(this, msg, ToastLength.Short).Show();
                            
                            
                        });*/
                        // new
                        string url = result.Text;
                    var response = await client.GetAsync(url + prefs.GetString("username", ""));
                    var res = await response.Content.ReadAsStringAsync();

                    if (res.Equals("Thank You."))
                    {
                        gridLayout.Visibility = Android.Views.ViewStates.Visible;
                        machine = result.Text;
                            //helloUser.SetText(("Hello " + user + "! You are working on machine " + machine).ToCharArray(), 0, user.Length + 6 + machine.Length + "! You are working on machine ".Length);
                            startTrainingBtn.Visibility = Android.Views.ViewStates.Gone;
                        logoutBtn.Visibility = Android.Views.ViewStates.Gone;

                        stopTrainingBtn.Visibility = Android.Views.ViewStates.Visible;
                        editor.PutString("machine", result.Text);
                        editor.Apply();        // applies changes asynchronously on newer APIs                              
                            timer.Start();
                        repsTimer.Start();
                    }
                    else
                    {
                        this.RunOnUiThread(() =>
                        {
                            Toast.MakeText(this, "Couldn't recognize the QR code", ToastLength.Short).Show();
                        });
                    }
                }

            });
            alert.SetNegativeButton("Cancel", (senderAlert, args) =>
            {
            });
            Dialog dialog = alert.Create();
            dialog.Show();

        }
        private void Timer_Elapsed(object sender, ElapsedEventArgs e)
        {
            millisecond++;
            if (millisecond > 1000)
            {
                secs++;
                millisecond = 0;
            }
            if (secs == 59)
            {
                mins++;
                secs = 0;
            }
            RunOnUiThread(() => {
                timerTxt.Text = String.Format("{0}:{1:00}:{2:000}", mins, secs, millisecond);
            });
        }
        private async void RepsTimer_ElapsedAsync(object sender, ElapsedEventArgs e)
        {
            var response = await client.GetAsync("http://40.113.134.7/APP/Visualise/usercurrentsession/numberofrepeats/?username=" + prefs.GetString("username", ""));
            var res = await response.Content.ReadAsStringAsync();
            if(res.Equals(" "))
            {
                return;
            }
            RunOnUiThread(() => {
                if (totalReps < Int32.Parse(res))
                {
                    if(repsNotChangedCounter*500 >= 15000)
                    {
                        lastTotalReps = totalReps;
                        setsNum++;
                    }
                    else
                    {
                        if (setsNum == 0)
                            setsNum++;
                    }
                    repsNotChangedCounter = 0;
                    totalReps = Int32.Parse(res);
                    
                }
                else // no change in reps
                {
                    repsNotChangedCounter++;
                }
                totalRepsTxt.Text = res;
                repsTxt.Text = (totalReps - lastTotalReps).ToString();
                setsTxt.Text = setsNum.ToString();
            });
        }


        void OnStopTraining(object sender, EventArgs e)
        {
            timer.Stop();
            repsTimer.Stop();
            AlertDialog.Builder alert = new AlertDialog.Builder(this);
            alert.SetTitle("Finish training");
            alert.SetMessage("Are you sure you want to finish training on this machine?");
            alert.SetPositiveButton("YES", async delegate
            {
                var response = await client.GetAsync(prefs.GetString("machine", "").Replace("starttraining", "stoptraining") + prefs.GetString("username", "") + "&sets=" + setsNum + "&repeats=" + totalReps);
                var res = await response.Content.ReadAsStringAsync();
                if (res.Equals("Done"))
                {
                    gridLayout.Visibility = Android.Views.ViewStates.Gone;
                    logoutBtn.Visibility = Android.Views.ViewStates.Visible;
                    helloUser.SetText(("Hello " + user).ToCharArray(), 0, user.Length + 6);
                    startTrainingBtn.Visibility = Android.Views.ViewStates.Visible;
                    stopTrainingBtn.Visibility = Android.Views.ViewStates.Gone;
                    editor.Remove("machine");
                    editor.Apply();        // applies changes asynchronously on newer APIs
                    AlertDialog.Builder alert2 = new AlertDialog.Builder(this);
                    alert.SetTitle("Your Workout");
                    //alert.SetMessage("Wrong username or password.");
                    alert.SetMessage("Do you want to see details about your training session?");
                    alert.SetPositiveButton("Yes", (senderAlert, args) =>
                    {

                        editor.PutString("prevActivity", "UserActivity");
                        editor.Apply();
                        
                        StartActivity(typeof(ImageVis));
                    });
                       
                    alert.SetNegativeButton("No thanks", (senderAlert, args) => { });
                    Dialog dialog2 = alert.Create();
                    dialog2.Show();
                }
                else
                {
                    AlertDialog.Builder alert2 = new AlertDialog.Builder(this);
                    alert.SetTitle("NETWORK FAILURE");
                    //alert.SetMessage("Wrong username or password.");
                    alert.SetMessage(response.ReasonPhrase.ToString());
                    alert.SetPositiveButton("Try again", (senderAlert, args) =>
                    {
                    });
                    Dialog dialog2 = alert.Create();
                    dialog2.Show();
  
                }
                
            });
            alert.SetNegativeButton("Cancel", (senderAlert, args) =>
            {
                timer.Start();
            });
            Dialog dialog = alert.Create();
            dialog.Show();

        }
    }
}