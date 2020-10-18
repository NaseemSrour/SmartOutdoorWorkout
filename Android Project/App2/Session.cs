using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;

namespace App2
{



    public class Session
    {
        public string Id
        {
            get;
            set;
        }
        public string Description
        {
            get;
            set;
        }
    }

    public class SessionAdapter : BaseAdapter<Session>
    {
        public List<Session> sList;
        private Context sContext;
        public SessionAdapter(Context context, List<Session> list)
        {
            sList = list;
            sContext = context;
        }
        public override Session this[int position]
        {
            get
            {
                return sList[position];
            }
        }
        public override int Count
        {
            get
            {
                return sList.Count;
            }
        }
        public override long GetItemId(int position)
        {
            return position;
        }
        public override View GetView(int position, View convertView, ViewGroup parent)
        {
            View row = convertView;
            try
            {
                if (row == null)
                {
                    row = LayoutInflater.From(sContext).Inflate(Resource.Layout.history_activity, null, false);
                }
                TextView txtName = row.FindViewById<TextView>(Resource.Id.sessionTxt);
                txtName.Text = sList[position].Description;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
            }
            finally { }
            return row;
        }
    }

}