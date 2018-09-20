using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ToolUpdater
{
    public partial class Form1 : Form
    {
        class Tool
        {
            public string name;
            public string desc;
            public string example;
            public string category;
            public string customInput;
            public string cmd;
            public string parser;
        }

        private List<Tool> _tools = new List<Tool>();
        private string _profile = string.Empty;

        public Form1()
        {
            InitializeComponent();

            _profile = cmbProfile.SelectedItem.ToString();
            LoadProfile();

            this.Text = "Total Count: : " + lsvMain.Items.Count.ToString();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (ddlCategory.SelectedItem == null)
            {
                MessageBox.Show("Need Category.");
                return;
            }

            var cat = ddlCategory.SelectedItem.ToString();
            cat = cat.Substring(cat.IndexOf("=") + 1).Trim();

            foreach (var tool in _tools)
            {
                if (tool.name == txtName.Text && tool.category == cat)
                {
                    Clear();
                    this.Text = "Duplicate Tool" + "\t\tTotal Count: : " + lsvMain.Items.Count.ToString();
                    return;
                }
            }

            var newTool = new Tool()
            {
                category = cat,
                cmd = txtCmd.Text.Replace("   ", " ").Replace("  ", " ").Trim(),
                desc = txtDesc.Text.Trim(),
                example = txtExample.Text.Trim(),
                name = txtName.Text.Trim(),
                customInput = txtCustomInput.Text.Trim(),
                parser = ddlParser.SelectedItem == null ? string.Empty : ddlParser.SelectedItem.ToString()
            };

            _tools.Add(newTool);

            var item = new ListViewItem()
            {
                Text = newTool.name,
                Tag = newTool
            };

            lsvMain.Items.Add(item);
            this.Text = "Added: " + newTool.name + "      Total Count: : " + lsvMain.Items.Count.ToString();
            Clear();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Export();
        }

        private string GetProfileFileName()
        {
            var fileName = string.Empty;

            //_profile = cmbProfile.SelectedItem.ToString();
            fileName = "./tools.json";
            if (_profile == "Windows")
            {
                fileName = "./tools_win.json";
            }

            return fileName;
        }

        private void Export()
        {
            var fileName = GetProfileFileName();
            // serialize JSON to a string and then write string to a file
            File.WriteAllText(fileName, JsonConvert.SerializeObject(_tools, Formatting.Indented));
        }

        private void LoadProfile()
        {
            var fileName = GetProfileFileName();

            _tools.Clear();
            if (System.IO.File.Exists(fileName))
            {
                System.IO.File.Copy(fileName, fileName.Replace(".json", "") + DateTime.Now.ToString("yyyy-MM-dd HH.mm.ss") + ".json");

                // read file into a string and deserialize JSON to a type
                _tools = JsonConvert.DeserializeObject<List<Tool>>(File.ReadAllText(fileName));
            }

            if (_tools == null)
            {
                _tools = new List<Tool>();
            }

            lsvMain.Items.Clear();
            foreach (var tool in _tools.OrderBy(t => t.name))
            {
                tool.cmd = tool.cmd.Replace("   ", " ").Replace("  ", " ");     // Cleanup some extra spaces.

                var item = new ListViewItem(tool.name)
                {
                    Text = tool.name,
                    Tag = tool
                };

                lsvMain.Items.Add(item);
            }
        }

        private void Clear()
        {
            txtCmd.Text = string.Empty;
            txtDesc.Text = string.Empty;
            txtExample.Text = string.Empty;
            txtName.Text = string.Empty;
            txtCustomInput.Text = string.Empty;
            ddlParser.SelectedItem = string.Empty;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Clear();
        }

        private void lsvMain_MouseClick(object sender, MouseEventArgs e)
        {
            if (lsvMain.SelectedItems.Count == 0)
            {
                return;
            }

            var tool = (Tool)lsvMain.SelectedItems[0].Tag;
            if (tool != null)
            {
                txtCmd.Text = tool.cmd;
                txtDesc.Text = tool.desc;
                txtExample.Text = tool.example;
                txtName.Text = tool.name;
                ddlCategory.SelectedItem = GetFullCategory(tool.category);
                txtCustomInput.Text = tool.customInput;
                ddlParser.SelectedItem = tool.parser;
            }
        }

        private string GetFullCategory(string num)
        {
            /*
                Enumeration = 1
                VulnerabilityScanner = 2
                Exploit = 3
                Web = 4
                StressTest = 5
                Forensics = 6
                Wireless = 7
                SniffingSpoofing = 8
                Password = 9
                Maintaining = 10
                ReverseEng = 11
                Reporting = 12
                Hardware = 13
            */

            if (num == "1")
                return "Enumeration = 1";
            else if (num == "2")
                return "VulnerabilityScanner = 2";
            else if (num == "3")
                return "Exploit = 3";
            else if (num == "4")
                return "Web = 4";
            else if (num == "5")
                return "StressTest = 5";
            else if (num == "6")
                return "Forensics = 6";
            else if (num == "7")
                return "Wireless = 7";
            else if (num == "8")
                return "SniffingSpoofing = 8";
            else if (num == "9")
                return "Password = 9";
            else if (num == "10")
                return "Maintaining = 10";
            else if (num == "11")
                return "ReverseEng = 11";
            else if (num == "12")
                return "Reporting = 12";
            else if (num == "13")
                return "Hardware = 13";

            return "";
        }

        private void button3_Click(object sender, EventArgs e)
        {
            Export();
        }

        private void UpdateCmdTextbox(string insert)
        {
            txtCmd.SelectedText = string.Empty;
            txtCmd.Text = txtCmd.Text.Insert(txtCmd.SelectionStart, " " + insert + " ");
        }

        private void label6_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label6.Text);
        }

        private void label7_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label7.Text);
        }

        private void label8_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label8.Text);
        }

        private void label9_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label9.Text);
        }

        private void label10_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label10.Text);
        }

        private void label11_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label11.Text);
        }

        private void label12_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label12.Text);
        }

        private void label13_Click(object sender, EventArgs e)
        {
            int i = 1;
            while (true)
            {
                if (txtCmd.Text.Contains("${arg" + i.ToString() + "}"))
                {
                    i++;
                }
                else
                {
                    break;
                }
            }
            var arg = "${arg" + i.ToString() + "}";
            UpdateCmdTextbox(arg);
            txtCustomInput.Text += "XXX=" + arg + ",";
        }

        private void label15_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label15.Text);
        }

        private void cmbProfile_SelectedIndexChanged(object sender, EventArgs e)
        {
            Export();
            _profile = cmbProfile.SelectedItem.ToString();
            LoadProfile();
        }
    }
}
