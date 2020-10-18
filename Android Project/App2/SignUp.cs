using Android.App;

using Android.OS;
using Android.Widget;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace App2

{

    [Activity(Label = "Sign Up")]
    public class SignUpActivity : Activity

    {

        EditText txtUserName, txtPassword, txtFirstName, txtLastName;
        NumberPicker ageNP, weightNP, heightNP;

        private static readonly HttpClient client = new HttpClient();
        protected override void OnCreate(Bundle bundle)

        {

            base.OnCreate(bundle);
            // Set our view from the "signup" layout resource
            SetContentView(Resource.Layout.signup);

            txtUserName = FindViewById<EditText>(Resource.Id.txtUser);
            txtPassword = FindViewById<EditText>(Resource.Id.txtPass);
            txtFirstName = FindViewById<EditText>(Resource.Id.txtFirstName);
            txtLastName = FindViewById<EditText>(Resource.Id.txtLastName);
            ageNP = FindViewById<NumberPicker>(Resource.Id.agePicker);
            weightNP = FindViewById<NumberPicker>(Resource.Id.WeightPicker);
            heightNP = FindViewById<NumberPicker>(Resource.Id.HeightPicker);
            
            Button signupBtn = FindViewById<Button>(Resource.Id.signupBtn);

            ageNP.MinValue = 1;
            ageNP.MaxValue = 120;
            weightNP.MinValue = 10;
            weightNP.MaxValue = 250;
            heightNP.MinValue = 10;
            heightNP.MaxValue = 250;
            ageNP.Value = 30;
            weightNP.Value = 70;
            heightNP.Value = 160;
            signupBtn.Click += OnSignup;
        }
        

    async void OnSignup(object sender, EventArgs e)
    
        {
            string sUserName = txtUserName.Text;
            string sPassword = txtPassword.Text;
            string sFirstName = txtFirstName.Text;
            string sLastName = txtLastName.Text;
            string sAge = ageNP.Value.ToString();
            string sWeight = weightNP.Value.ToString();
            string sHeight = heightNP.Value.ToString();


            //Pass details to db
            string sContentType = "application/json"; // or application/xml

            JObject oJsonObject = new JObject();
            oJsonObject.Add("username", sUserName);
            oJsonObject.Add("password", sPassword);
                       oJsonObject.Add("firstname", sFirstName);
            oJsonObject.Add("lastname", sLastName);
            oJsonObject.Add("age", sAge);
            oJsonObject.Add("weight", sWeight);
            oJsonObject.Add("height", sHeight);


            var response = await client.PostAsync("http://40.113.134.7/APP/signup/", new StringContent(oJsonObject.ToString(), Encoding.UTF8, sContentType));
            var res = await response.Content.ReadAsStringAsync();

            if (res.Equals("User Added Successfully"))
            {
                AlertDialog.Builder alert = new AlertDialog.Builder(this);
                alert.SetTitle("SUCCESS");
                alert.SetMessage("Sign up successful, Please log in.");
                alert.SetPositiveButton("OK", (senderAlert, args) => {
                    StartActivity(typeof(MainActivity));
                });
                Dialog dialog = alert.Create();
                dialog.Show();
            }
            else 
            {
                AlertDialog.Builder alert = new AlertDialog.Builder(this);
                alert.SetTitle("FAILURE");
                alert.SetMessage(res);
                alert.SetPositiveButton("OK", (senderAlert, args) => {
                });
                Dialog dialog = alert.Create();
                dialog.Show();
            }

        }

    }

}