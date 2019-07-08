using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using Newtonsoft.Json;

namespace DataCreator
{
    public partial class ChecklistCtl : UserControl
    {
        private const string CHECKLIST_FILE = "checklists.json";

        class ChecklistItem
        {
            public ChecklistItem(string entry, List<string> steps, string codeBlock)
            {
                this.entry = entry;
                this.codeBlock = codeBlock;
                this.steps = steps;
            }

            public string entry { get; set; }
            public List<string> steps { get; set; }
            public string codeBlock { get; set; }
        }

        class Checklist
        {
            public Checklist(string name)
            {
                this.name = name;
                this.items = new List<ChecklistItem>();
            }

            public string name { get; set; }
            public List<ChecklistItem> items { get; set; }
        }

        private Checklist _currentChecklist = null;

        public ChecklistCtl()
        {
            InitializeComponent();

            LoadChecklists();
            LoadChecklistItems();
        }

        private void LoadChecklists()
        {
            try
            {
                var checklists = new List<Checklist>();

                if (File.Exists(CHECKLIST_FILE))
                {
                    File.Copy(CHECKLIST_FILE, CHECKLIST_FILE.Replace(".json", "") + DateTime.Now.ToString("yyyy-MM-dd HH.mm.ss") + ".json");

                    // read file into a string and deserialize JSON to a type
                    checklists = JsonConvert.DeserializeObject<List<Checklist>>(File.ReadAllText(CHECKLIST_FILE));
                }

                lsvMain.Items.Clear();
                foreach (var checklist in checklists.OrderBy(c => c.name))
                {
                    var item = new ListViewItem(checklist.name)
                    {
                        Text = checklist.name,
                        Tag = checklist
                    };

                    lsvMain.Items.Add(item);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void LoadChecklistItems()
        {
            lsvItems.Items.Clear();
            if (_currentChecklist != null)
            {
                foreach (var checklistItem in _currentChecklist.items)
                {
                    var item = new ListViewItem(checklistItem.entry)
                    {
                        Text = checklistItem.entry,
                        Tag = checklistItem
                    };

                    lsvItems.Items.Add(item);
                }
            }
            Clear();
        }

        private void LoadItem()
        {
            if (lsvItems.SelectedItems.Count != 0)
            {
                var checklistItem = (ChecklistItem)lsvItems.SelectedItems[0].Tag;
                if (checklistItem != null)
                {
                    txtCodeBlock.Text = checklistItem.codeBlock;
                    txtEntry.Text = checklistItem.entry;
                    txtSteps.Text = string.Empty;

                    if (checklistItem.steps != null)
                    {
                        checklistItem.steps.ForEach(s => txtSteps.Text += s + Environment.NewLine);
                    }
                }
            }
        }

        private void Clear()
        {
            txtCodeBlock.Text = string.Empty;
            txtEntry.Text = string.Empty;
            txtSteps.Text = string.Empty;
        }

        private void lsvMain_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (lsvMain.SelectedItems.Count != 0)
            {
                var checklist = (Checklist)lsvMain.SelectedItems[0].Tag;
                if (checklist != null)
                {
                    _currentChecklist = checklist;

                }
            }
            LoadChecklistItems();
        }

        private void btnAddItem_Click(object sender, EventArgs e)
        {
            if (_currentChecklist == null)
            {
                MessageBox.Show("Select checklist first.");
                return;
            }

            _currentChecklist.items.Add(new ChecklistItem(txtEntry.Text.Trim(), txtSteps.Text.Split(new[] { Environment.NewLine }, StringSplitOptions.None).ToList(), txtCodeBlock.Text.Trim()));
            LoadChecklistItems();
            txtEntry.Text = string.Empty;
            txtSteps.Text = string.Empty;
            txtCodeBlock.Text = string.Empty;
        }

        private void btnAddChecklist_Click(object sender, EventArgs e)
        {
            var name = txtChecklistName.Text.Trim();
            if (string.IsNullOrEmpty(name))
            {
                MessageBox.Show("Name it first.");
                return;
            }

            foreach (ListViewItem item in lsvMain.Items)
            {
                if (((Checklist)item.Tag).name.ToLower() == name.ToLower())
                {
                    MessageBox.Show("Checklist with that name exists.");
                    return;
                }
            }

            var checklist = new Checklist(name);
            var listItem = new ListViewItem(checklist.name)
            {
                Text = checklist.name,
                Tag = checklist
            };

            lsvMain.Items.Add(listItem);
        }

        public void Export()
        {
            var checklist = new List<Checklist>();
            foreach (ListViewItem item in lsvMain.Items)
            {
                checklist.Add((Checklist)item.Tag);
            }

            File.WriteAllText(CHECKLIST_FILE, JsonConvert.SerializeObject(checklist, Formatting.Indented));
        }

        private void UpdateCmdTextbox(string insert)
        {
            txtSteps.SelectedText = string.Empty;
            txtSteps.Text = txtSteps.Text.Insert(txtSteps.SelectionStart, " " + insert + " ");
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            Export();
        }

        private void lblTarget_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(lblTarget.Text);
        }

        private void lblUser_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(lblUser.Text);
        }

        private void lblPass_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(lblPass.Text);
        }

        private void lblWorking_Click(object sender, EventArgs e)
        {
            UpdateCmdTextbox(lblWorking.Text);
        }

        private void lsvItems_SelectedIndexChanged(object sender, EventArgs e)
        {
            LoadItem();
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            if (lsvItems.SelectedItems.Count != 0)
            {
                var checklistItem = (ChecklistItem)lsvItems.SelectedItems[0].Tag;
                if (checklistItem != null)
                {
                    checklistItem.codeBlock = txtCodeBlock.Text;
                    checklistItem.entry = txtEntry.Text;
                    var item = new ChecklistItem(txtEntry.Text.Trim(), txtSteps.Text.Split(new[] { Environment.NewLine }, StringSplitOptions.None).ToList(), txtCodeBlock.Text.Trim());


                    _currentChecklist.items[lsvItems.SelectedItems[0].Index] = item;
                    LoadChecklistItems();
                }
            }
        }

        private void btnChecklistUp_Click(object sender, EventArgs e)
        {
            if (lsvMain.SelectedItems.Count != 0 && lsvMain.SelectedItems[0].Index > 0)
            {
                var bottomIndex = lsvMain.SelectedItems[0].Index;
                var topIndex = bottomIndex - 1;

                var bottomChecklist = (Checklist)lsvMain.SelectedItems[0].Tag;
                var topChecklist = (Checklist)lsvMain.Items[topIndex].Tag;

                var bottomItem = new ListViewItem(bottomChecklist.name)
                {
                    Text = bottomChecklist.name,
                    Tag = bottomChecklist
                };

                var topItem = new ListViewItem(topChecklist.name)
                {
                    Text = topChecklist.name,
                    Tag = topChecklist
                };

                if (bottomChecklist != null && topChecklist != null)
                {
                    lsvMain.Items.RemoveAt(topIndex);
                    lsvMain.Items.Insert(topIndex, bottomItem);

                    lsvMain.Items.RemoveAt(bottomIndex);
                    lsvMain.Items.Insert(bottomIndex, topItem);
                }
            }
        }

        private void btnChecklistDown_Click(object sender, EventArgs e)
        {
            if (lsvMain.SelectedItems.Count != 0 && lsvMain.SelectedItems[0].Index < (lsvMain.Items.Count - 1))
            {
                var topIndex = lsvMain.SelectedItems[0].Index;
                var bottomIndex = topIndex + 1;

                var topChecklist = (Checklist)lsvMain.SelectedItems[0].Tag;
                var bottomChecklist = (Checklist)lsvMain.Items[bottomIndex].Tag;

                var topItem = new ListViewItem(topChecklist.name)
                {
                    Text = topChecklist.name,
                    Tag = topChecklist
                };

                var bottomItem = new ListViewItem(bottomChecklist.name)
                {
                    Text = bottomChecklist.name,
                    Tag = bottomChecklist
                };

                if (bottomChecklist != null && topChecklist != null)
                {
                    lsvMain.Items.RemoveAt(bottomIndex);
                    lsvMain.Items.Insert(bottomIndex, topItem);

                    lsvMain.Items.RemoveAt(topIndex);
                    lsvMain.Items.Insert(topIndex, bottomItem);
                }
            }
        }

        private void btnUp_Click(object sender, EventArgs e)
        {
            if (lsvItems.SelectedItems.Count != 0 && lsvItems.SelectedItems[0].Index > 0)
            {
                var bottomIndex = lsvItems.SelectedItems[0].Index;
                var topIndex = bottomIndex - 1;

                var bottomChecklist = (ChecklistItem)lsvItems.SelectedItems[0].Tag;
                var topChecklist = (ChecklistItem)lsvItems.Items[topIndex].Tag;

                var bottomItem = new ListViewItem(bottomChecklist.entry)
                {
                    Text = bottomChecklist.entry,
                    Tag = bottomChecklist
                };

                var topItem = new ListViewItem(topChecklist.entry)
                {
                    Text = topChecklist.entry,
                    Tag = topChecklist
                };

                if (bottomChecklist != null && topChecklist != null)
                {
                    lsvItems.Items.RemoveAt(topIndex);
                    lsvItems.Items.Insert(topIndex, bottomItem);

                    lsvItems.Items.RemoveAt(bottomIndex);
                    lsvItems.Items.Insert(bottomIndex, topItem);
                }
            }
        }

        private void btnDown_Click(object sender, EventArgs e)
        {
            if (lsvItems.SelectedItems.Count != 0 && lsvItems.SelectedItems[0].Index < (lsvItems.Items.Count - 1))
            {
                var topIndex = lsvItems.SelectedItems[0].Index;
                var bottomIndex = topIndex + 1;

                var topChecklist = (ChecklistItem)lsvItems.SelectedItems[0].Tag;
                var bottomChecklist = (ChecklistItem)lsvItems.Items[bottomIndex].Tag;

                var topItem = new ListViewItem(topChecklist.entry)
                {
                    Text = topChecklist.entry,
                    Tag = topChecklist
                };

                var bottomItem = new ListViewItem(bottomChecklist.entry)
                {
                    Text = bottomChecklist.entry,
                    Tag = bottomChecklist
                };

                if (bottomChecklist != null && topChecklist != null)
                {
                    lsvItems.Items.RemoveAt(bottomIndex);
                    lsvItems.Items.Insert(bottomIndex, topItem);

                    lsvItems.Items.RemoveAt(topIndex);
                    lsvItems.Items.Insert(topIndex, bottomItem);
                }
            }
        }
    }
}
