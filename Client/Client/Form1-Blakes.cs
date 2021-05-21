using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;

namespace Client
{
    public partial class Form1 : Form
    {
        int port;
        int byteCount;
        NetworkStream stream;
        byte[] sendData;
        TcpClient client;

        //create the stopwatch
        System.Diagnostics.Stopwatch StopWatch = new System.Diagnostics.Stopwatch();

        public Form1()
        {
            InitializeComponent();
        }

        private void toolStripButton2_Click(object sender, EventArgs e)
        {
            timer1.Stop();

            SendMessage(textBox1.Text);

            //record time andmessage


            this.StopWatch.Reset();
            timer1.Start();
        }

        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            if(!int.TryParse(textBox3.Text, out port))
            {
                MessageBox.Show("Port number not valied");
                OutPut.Items.Add("Port number invalied");
            }

            try
            {
                client = new TcpClient(textBox2.Text, port);
                MessageBox.Show("Connection Made");
                OutPut.Items.Add($"Made Connection with {textBox2.Text}");
            }
            catch(SocketException)
            {
                MessageBox.Show("Connection Failed");
                OutPut.Items.Add($"Connection Failed");
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            TimeSpan elapsed = this.StopWatch.Elapsed;
            OutPut.Items.Add(string.Format("{0:00}:{1:00}:{2:00}:{3:00}", Math.Floor(elapsed.TotalHours), elapsed.Minutes, elapsed.Seconds, elapsed.Milliseconds));
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            SendMessage("mtr" + Speed.Value.ToString().PadLeft(3));

            if(Speed.Value == 0)
            {
                SendMessage("mtrstp");
            }
            else
            {
                SendMessage("mtrrun");
            }
        }

        private void Steering_Scroll(object sender, EventArgs e)
        {
            SendMessage("ser" + Steering.Value.ToString().PadLeft(3));
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (Forward.Checked)
            {
                SendMessage("mtrbac");
            }
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (Backward.Checked)
            {
                SendMessage("mtrfor");
            }
        }

        private void Stop_Click(object sender, EventArgs e)
        {
            SendMessage("mtrstp");
        }

        private void SendMessage(string message)
        {
            try
            {
                byteCount = Encoding.ASCII.GetByteCount(message);
                sendData = new byte[byteCount];
                sendData = Encoding.ASCII.GetBytes(message);
                stream = client.GetStream();
                stream.Write(sendData, 0, sendData.Length);

                OutPut.Items.Add($"Sent Data {message}");
            }
            catch (NullReferenceException)
            {
                MessageBox.Show("Failed to send");
            }
        }
    }
}
