using System;

namespace Client
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.toolStripButton1 = new System.Windows.Forms.ToolStripButton();
            this.toolStripButton2 = new System.Windows.Forms.ToolStripButton();
            this.toolStripButton3 = new System.Windows.Forms.ToolStripButton();
            this.textBox3 = new System.Windows.Forms.TextBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.OutPut = new System.Windows.Forms.ListBox();
            this.label2 = new System.Windows.Forms.Label();
            this.SteeringLabel = new System.Windows.Forms.Label();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.Speed = new System.Windows.Forms.TrackBar();
            this.Steering = new System.Windows.Forms.TrackBar();
            this.label5 = new System.Windows.Forms.Label();
            this.Forward = new System.Windows.Forms.RadioButton();
            this.Backward = new System.Windows.Forms.RadioButton();
            this.Stop = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.Exit = new System.Windows.Forms.Button();
            this.toolStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.Speed)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.Steering)).BeginInit();
            this.SuspendLayout();
            // 
            // toolStrip1
            // 
            this.toolStrip1.ImageScalingSize = new System.Drawing.Size(24, 24);
            this.toolStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripButton1,
            this.toolStripButton2,
            this.toolStripButton3});
            this.toolStrip1.Location = new System.Drawing.Point(0, 0);
            this.toolStrip1.Name = "toolStrip1";
            this.toolStrip1.Padding = new System.Windows.Forms.Padding(0, 0, 2, 0);
            this.toolStrip1.Size = new System.Drawing.Size(800, 25);
            this.toolStrip1.TabIndex = 0;
            this.toolStrip1.Text = "toolStrip1";
            // 
            // toolStripButton1
            // 
            this.toolStripButton1.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.toolStripButton1.Image = ((System.Drawing.Image)(resources.GetObject("toolStripButton1.Image")));
            this.toolStripButton1.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolStripButton1.Name = "toolStripButton1";
            this.toolStripButton1.Size = new System.Drawing.Size(56, 22);
            this.toolStripButton1.Text = "Connect";
            this.toolStripButton1.Click += new System.EventHandler(this.toolStripButton1_Click);
            // 
            // toolStripButton2
            // 
            this.toolStripButton2.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.toolStripButton2.Image = ((System.Drawing.Image)(resources.GetObject("toolStripButton2.Image")));
            this.toolStripButton2.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolStripButton2.Name = "toolStripButton2";
            this.toolStripButton2.Size = new System.Drawing.Size(37, 22);
            this.toolStripButton2.Text = "Send";
            this.toolStripButton2.Click += new System.EventHandler(this.toolStripButton2_Click);
            // 
            // toolStripButton3
            // 
            this.toolStripButton3.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.toolStripButton3.Image = ((System.Drawing.Image)(resources.GetObject("toolStripButton3.Image")));
            this.toolStripButton3.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolStripButton3.Name = "toolStripButton3";
            this.toolStripButton3.Size = new System.Drawing.Size(70, 22);
            this.toolStripButton3.Text = "Disconnect";
            // 
            // textBox3
            // 
            this.textBox3.Location = new System.Drawing.Point(523, 28);
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(251, 20);
            this.textBox3.TabIndex = 3;
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(92, 28);
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(262, 20);
            this.textBox2.TabIndex = 4;
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(92, 63);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(682, 20);
            this.textBox1.TabIndex = 5;
            // 
            // OutPut
            // 
            this.OutPut.FormattingEnabled = true;
            this.OutPut.Location = new System.Drawing.Point(12, 210);
            this.OutPut.Name = "OutPut";
            this.OutPut.Size = new System.Drawing.Size(776, 225);
            this.OutPut.TabIndex = 6;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(479, 31);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(26, 13);
            this.label2.TabIndex = 8;
            this.label2.Text = "Port";
            // 
            // SteeringLabel
            // 
            this.SteeringLabel.AutoSize = true;
            this.SteeringLabel.Location = new System.Drawing.Point(71, 171);
            this.SteeringLabel.Name = "SteeringLabel";
            this.SteeringLabel.Size = new System.Drawing.Size(46, 13);
            this.SteeringLabel.TabIndex = 9;
            this.SteeringLabel.Text = "Steering";
            // 
            // timer1
            // 
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // Speed
            // 
            this.Speed.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.Speed.Location = new System.Drawing.Point(691, 93);
            this.Speed.Maximum = 100;
            this.Speed.Name = "Speed";
            this.Speed.Orientation = System.Windows.Forms.Orientation.Vertical;
            this.Speed.Size = new System.Drawing.Size(45, 104);
            this.Speed.TabIndex = 10;
            this.Speed.Scroll += new System.EventHandler(this.trackBar1_Scroll);
            // 
            // Steering
            // 
            this.Steering.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.Steering.Location = new System.Drawing.Point(43, 123);
            this.Steering.Minimum = 4;
            this.Steering.Name = "Steering";
            this.Steering.Size = new System.Drawing.Size(104, 45);
            this.Steering.TabIndex = 11;
            this.Steering.Value = 7;
            this.Steering.Scroll += new System.EventHandler(this.Steering_Scroll);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(742, 131);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(37, 13);
            this.label5.TabIndex = 13;
            this.label5.Text = "Power";
            // 
            // Forward
            // 
            this.Forward.AutoSize = true;
            this.Forward.Checked = true;
            this.Forward.Location = new System.Drawing.Point(612, 100);
            this.Forward.Name = "Forward";
            this.Forward.Size = new System.Drawing.Size(63, 17);
            this.Forward.TabIndex = 14;
            this.Forward.TabStop = true;
            this.Forward.Text = "Forward";
            this.Forward.UseVisualStyleBackColor = true;
            this.Forward.CheckedChanged += new System.EventHandler(this.radioButton1_CheckedChanged);
            // 
            // Backward
            // 
            this.Backward.AutoSize = true;
            this.Backward.Location = new System.Drawing.Point(612, 123);
            this.Backward.Name = "Backward";
            this.Backward.Size = new System.Drawing.Size(73, 17);
            this.Backward.TabIndex = 15;
            this.Backward.Text = "Backward";
            this.Backward.UseVisualStyleBackColor = true;
            this.Backward.CheckedChanged += new System.EventHandler(this.radioButton2_CheckedChanged);
            // 
            // Stop
            // 
            this.Stop.Location = new System.Drawing.Point(610, 171);
            this.Stop.Name = "Stop";
            this.Stop.Size = new System.Drawing.Size(75, 23);
            this.Stop.TabIndex = 16;
            this.Stop.Text = "Stop";
            this.Stop.UseVisualStyleBackColor = true;
            this.Stop.Click += new System.EventHandler(this.Stop_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(40, 66);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(50, 13);
            this.label1.TabIndex = 17;
            this.label1.Text = "Message";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(14, 31);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(72, 13);
            this.label3.TabIndex = 18;
            this.label3.Text = "IP/HostName";
            // 
            // Exit
            // 
            this.Exit.Location = new System.Drawing.Point(529, 171);
            this.Exit.Name = "Exit";
            this.Exit.Size = new System.Drawing.Size(75, 23);
            this.Exit.TabIndex = 19;
            this.Exit.Text = "Exit";
            this.Exit.UseVisualStyleBackColor = true;
            this.Exit.Click += new System.EventHandler(this.Exit_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.Exit);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.Stop);
            this.Controls.Add(this.Backward);
            this.Controls.Add(this.Forward);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.Steering);
            this.Controls.Add(this.Speed);
            this.Controls.Add(this.SteeringLabel);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.OutPut);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.textBox2);
            this.Controls.Add(this.textBox3);
            this.Controls.Add(this.toolStrip1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.toolStrip1.ResumeLayout(false);
            this.toolStrip1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.Speed)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.Steering)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.ToolStripButton toolStripButton1;
        private System.Windows.Forms.ToolStripButton toolStripButton2;
        private System.Windows.Forms.ToolStripButton toolStripButton3;
        private System.Windows.Forms.TextBox textBox3;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.ListBox OutPut;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label SteeringLabel;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.TrackBar Speed;
        private System.Windows.Forms.TrackBar Steering;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.RadioButton Forward;
        private System.Windows.Forms.RadioButton Backward;
        private System.Windows.Forms.Button Stop;
        private EventHandler listBox1_SelectedIndexChanged;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button Exit;
    }
}

