using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using System.IO;

namespace DataCreator
{
    public partial class ReverseShells : UserControl
    {
        private class Shell
        {
            public string name { get; set; }
            public string description { get; set; }
            public string code { get; set; }
        }

        private const string FILE_NAME = "reverse_shells.json";
        List<Shell> _shells = new List<Shell>();

        public ReverseShells()
        {
            InitializeComponent();
            LoadShells();
        }

        private void LoadShells()
        {
            _shells.Clear();
            if (File.Exists(FILE_NAME))
            {
                File.Copy(FILE_NAME, FILE_NAME.Replace(".json", "") + DateTime.Now.ToString("yyyy-MM-dd HH.mm.ss") + ".json");

                // read file into a string and deserialize JSON to a type
                _shells = JsonConvert.DeserializeObject<List<Shell>>(File.ReadAllText(FILE_NAME));
            }

            if (_shells == null)
            {
                _shells = new List<Shell>();
            }

            lsvMain.Items.Clear();
            foreach (var shell in _shells.OrderBy(t => t.name))
            {
                var item = new ListViewItem(shell.name)
                {
                    Text = shell.name,
                    Tag = shell
                };

                lsvMain.Items.Add(item);
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            foreach (var shell in _shells)
            {
                if (shell.name == txtName.Text)
                {
                    Clear();
                    this.Text = "Duplicate Tool" + "\t\tTotal Count: : " + lsvMain.Items.Count.ToString();
                    return;
                }
            }

            var newShell = new Shell()
            {
                name = txtName.Text.Trim(),
                description = txtDesc.Text.Trim(),
                code = txtLines.Text.Trim()
            };

            _shells.Add(newShell);

            var item = new ListViewItem()
            {
                Text = newShell.name,
                Tag = newShell
            };

            lsvMain.Items.Add(item);
            Clear();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Clear();
        }

        private void Clear()
        {
            txtDesc.Text = string.Empty;
            txtName.Text = string.Empty;
            txtLines.Text = string.Empty;
        }

        private void button3_Click(object sender, EventArgs e)
        {
            Export();
        }

        private void lsvMain_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (lsvMain.SelectedItems.Count == 0)
            {
                return;
            }

            var shell = (Shell)lsvMain.SelectedItems[0].Tag;
            if (shell != null)
            {
                txtDesc.Text = shell.description;
                txtName.Text = shell.name;
                txtLines.Text = shell.code;
            }
        }

        public void Export()
        {
            File.WriteAllText(FILE_NAME, JsonConvert.SerializeObject(_shells, Formatting.Indented));
        }

        private void UpdateCmdTextbox(string insert)
        {
            txtLines.SelectedText = string.Empty;
            txtLines.Text = txtLines.Text.Insert(txtLines.SelectionStart, " " + insert + " ");
        }

        private void label6_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label6.Text);
        }

        private void label11_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(label11.Text);
        }
    }
}
