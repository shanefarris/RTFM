namespace DataCreator
{
    partial class ChecklistCtl
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.btnChecklistDown = new System.Windows.Forms.Button();
            this.btnChecklistUp = new System.Windows.Forms.Button();
            this.btnUpdate = new System.Windows.Forms.Button();
            this.lblWorking = new System.Windows.Forms.Label();
            this.lblPass = new System.Windows.Forms.Label();
            this.lblUser = new System.Windows.Forms.Label();
            this.lblTarget = new System.Windows.Forms.Label();
            this.btnSave = new System.Windows.Forms.Button();
            this.btnDown = new System.Windows.Forms.Button();
            this.btnUp = new System.Windows.Forms.Button();
            this.label5 = new System.Windows.Forms.Label();
            this.txtChecklistName = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.txtCodeBlock = new System.Windows.Forms.TextBox();
            this.txtEntry = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.btnAddItem = new System.Windows.Forms.Button();
            this.btnAddChecklist = new System.Windows.Forms.Button();
            this.txtSteps = new System.Windows.Forms.TextBox();
            this.lsvItems = new System.Windows.Forms.ListView();
            this.lsvMain = new System.Windows.Forms.ListView();
            this.SuspendLayout();
            // 
            // btnChecklistDown
            // 
            this.btnChecklistDown.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnChecklistDown.Location = new System.Drawing.Point(3, 163);
            this.btnChecklistDown.Name = "btnChecklistDown";
            this.btnChecklistDown.Size = new System.Drawing.Size(64, 52);
            this.btnChecklistDown.TabIndex = 102;
            this.btnChecklistDown.Text = "Down";
            this.btnChecklistDown.UseVisualStyleBackColor = true;
            this.btnChecklistDown.Click += new System.EventHandler(this.btnChecklistDown_Click);
            // 
            // btnChecklistUp
            // 
            this.btnChecklistUp.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnChecklistUp.Location = new System.Drawing.Point(3, 3);
            this.btnChecklistUp.Name = "btnChecklistUp";
            this.btnChecklistUp.Size = new System.Drawing.Size(64, 52);
            this.btnChecklistUp.TabIndex = 101;
            this.btnChecklistUp.Text = "UP";
            this.btnChecklistUp.UseVisualStyleBackColor = true;
            this.btnChecklistUp.Click += new System.EventHandler(this.btnChecklistUp_Click);
            // 
            // btnUpdate
            // 
            this.btnUpdate.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnUpdate.Location = new System.Drawing.Point(973, 746);
            this.btnUpdate.Name = "btnUpdate";
            this.btnUpdate.Size = new System.Drawing.Size(126, 52);
            this.btnUpdate.TabIndex = 100;
            this.btnUpdate.Text = "Update";
            this.btnUpdate.UseVisualStyleBackColor = true;
            this.btnUpdate.Click += new System.EventHandler(this.btnUpdate_Click);
            // 
            // lblWorking
            // 
            this.lblWorking.AutoSize = true;
            this.lblWorking.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblWorking.Location = new System.Drawing.Point(969, 408);
            this.lblWorking.Name = "lblWorking";
            this.lblWorking.Size = new System.Drawing.Size(108, 20);
            this.lblWorking.TabIndex = 99;
            this.lblWorking.Text = "${working_dir}";
            this.lblWorking.Click += new System.EventHandler(this.lblWorking_Click);
            // 
            // lblPass
            // 
            this.lblPass.AutoSize = true;
            this.lblPass.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblPass.Location = new System.Drawing.Point(969, 379);
            this.lblPass.Name = "lblPass";
            this.lblPass.Size = new System.Drawing.Size(91, 20);
            this.lblPass.TabIndex = 98;
            this.lblPass.Text = "${pass_file}";
            this.lblPass.Click += new System.EventHandler(this.lblPass_Click);
            // 
            // lblUser
            // 
            this.lblUser.AutoSize = true;
            this.lblUser.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblUser.Location = new System.Drawing.Point(969, 350);
            this.lblUser.Name = "lblUser";
            this.lblUser.Size = new System.Drawing.Size(88, 20);
            this.lblUser.TabIndex = 97;
            this.lblUser.Text = "${user_file}";
            this.lblUser.Click += new System.EventHandler(this.lblUser_Click);
            // 
            // lblTarget
            // 
            this.lblTarget.AutoSize = true;
            this.lblTarget.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblTarget.Location = new System.Drawing.Point(969, 320);
            this.lblTarget.Name = "lblTarget";
            this.lblTarget.Size = new System.Drawing.Size(70, 20);
            this.lblTarget.TabIndex = 96;
            this.lblTarget.Text = "${target}";
            this.lblTarget.Click += new System.EventHandler(this.lblTarget_Click);
            // 
            // btnSave
            // 
            this.btnSave.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSave.Location = new System.Drawing.Point(1210, 746);
            this.btnSave.Name = "btnSave";
            this.btnSave.Size = new System.Drawing.Size(126, 52);
            this.btnSave.TabIndex = 88;
            this.btnSave.Text = "Save/Export";
            this.btnSave.UseVisualStyleBackColor = true;
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // 
            // btnDown
            // 
            this.btnDown.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnDown.Location = new System.Drawing.Point(1272, 163);
            this.btnDown.Name = "btnDown";
            this.btnDown.Size = new System.Drawing.Size(64, 52);
            this.btnDown.TabIndex = 90;
            this.btnDown.Text = "Down";
            this.btnDown.UseVisualStyleBackColor = true;
            this.btnDown.Click += new System.EventHandler(this.btnDown_Click);
            // 
            // btnUp
            // 
            this.btnUp.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnUp.Location = new System.Drawing.Point(1272, 3);
            this.btnUp.Name = "btnUp";
            this.btnUp.Size = new System.Drawing.Size(64, 52);
            this.btnUp.TabIndex = 89;
            this.btnUp.Text = "UP";
            this.btnUp.UseVisualStyleBackColor = true;
            this.btnUp.Click += new System.EventHandler(this.btnUp_Click);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(15, 276);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(89, 13);
            this.label5.TabIndex = 95;
            this.label5.Text = "Newline delimited";
            // 
            // txtChecklistName
            // 
            this.txtChecklistName.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtChecklistName.Location = new System.Drawing.Point(1062, 256);
            this.txtChecklistName.Name = "txtChecklistName";
            this.txtChecklistName.Size = new System.Drawing.Size(274, 26);
            this.txtChecklistName.TabIndex = 86;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(1005, 259);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(51, 20);
            this.label4.TabIndex = 94;
            this.label4.Text = "Name";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(14, 649);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(90, 20);
            this.label3.TabIndex = 93;
            this.label3.Text = "Code Block";
            // 
            // txtCodeBlock
            // 
            this.txtCodeBlock.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtCodeBlock.Location = new System.Drawing.Point(110, 566);
            this.txtCodeBlock.Multiline = true;
            this.txtCodeBlock.Name = "txtCodeBlock";
            this.txtCodeBlock.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtCodeBlock.Size = new System.Drawing.Size(853, 232);
            this.txtCodeBlock.TabIndex = 84;
            // 
            // txtEntry
            // 
            this.txtEntry.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtEntry.Location = new System.Drawing.Point(110, 221);
            this.txtEntry.Name = "txtEntry";
            this.txtEntry.Size = new System.Drawing.Size(853, 26);
            this.txtEntry.TabIndex = 82;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(53, 224);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(46, 20);
            this.label1.TabIndex = 91;
            this.label1.Text = "Entry";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(48, 256);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(51, 20);
            this.label2.TabIndex = 92;
            this.label2.Text = "Steps";
            // 
            // btnAddItem
            // 
            this.btnAddItem.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnAddItem.Location = new System.Drawing.Point(973, 686);
            this.btnAddItem.Name = "btnAddItem";
            this.btnAddItem.Size = new System.Drawing.Size(126, 52);
            this.btnAddItem.TabIndex = 85;
            this.btnAddItem.Text = "Add Item";
            this.btnAddItem.UseVisualStyleBackColor = true;
            this.btnAddItem.Click += new System.EventHandler(this.btnAddItem_Click);
            // 
            // btnAddChecklist
            // 
            this.btnAddChecklist.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnAddChecklist.Location = new System.Drawing.Point(1210, 288);
            this.btnAddChecklist.Name = "btnAddChecklist";
            this.btnAddChecklist.Size = new System.Drawing.Size(126, 52);
            this.btnAddChecklist.TabIndex = 87;
            this.btnAddChecklist.Text = "Add New Checklist";
            this.btnAddChecklist.UseVisualStyleBackColor = true;
            this.btnAddChecklist.Click += new System.EventHandler(this.btnAddChecklist_Click);
            // 
            // txtSteps
            // 
            this.txtSteps.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtSteps.Location = new System.Drawing.Point(110, 253);
            this.txtSteps.Multiline = true;
            this.txtSteps.Name = "txtSteps";
            this.txtSteps.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.txtSteps.Size = new System.Drawing.Size(853, 307);
            this.txtSteps.TabIndex = 83;
            // 
            // lsvItems
            // 
            this.lsvItems.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lsvItems.HeaderStyle = System.Windows.Forms.ColumnHeaderStyle.None;
            this.lsvItems.Location = new System.Drawing.Point(451, 3);
            this.lsvItems.MultiSelect = false;
            this.lsvItems.Name = "lsvItems";
            this.lsvItems.ShowGroups = false;
            this.lsvItems.Size = new System.Drawing.Size(815, 212);
            this.lsvItems.TabIndex = 81;
            this.lsvItems.UseCompatibleStateImageBehavior = false;
            this.lsvItems.View = System.Windows.Forms.View.List;
            this.lsvItems.SelectedIndexChanged += new System.EventHandler(this.lsvItems_SelectedIndexChanged);
            // 
            // lsvMain
            // 
            this.lsvMain.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lsvMain.HeaderStyle = System.Windows.Forms.ColumnHeaderStyle.None;
            this.lsvMain.Location = new System.Drawing.Point(73, 3);
            this.lsvMain.MultiSelect = false;
            this.lsvMain.Name = "lsvMain";
            this.lsvMain.ShowGroups = false;
            this.lsvMain.Size = new System.Drawing.Size(372, 212);
            this.lsvMain.TabIndex = 80;
            this.lsvMain.UseCompatibleStateImageBehavior = false;
            this.lsvMain.View = System.Windows.Forms.View.List;
            this.lsvMain.SelectedIndexChanged += new System.EventHandler(this.lsvMain_SelectedIndexChanged);
            // 
            // ChecklistCtl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.btnChecklistDown);
            this.Controls.Add(this.btnChecklistUp);
            this.Controls.Add(this.btnUpdate);
            this.Controls.Add(this.lblWorking);
            this.Controls.Add(this.lblPass);
            this.Controls.Add(this.lblUser);
            this.Controls.Add(this.lblTarget);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.btnDown);
            this.Controls.Add(this.btnUp);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.txtChecklistName);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txtCodeBlock);
            this.Controls.Add(this.txtEntry);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.btnAddItem);
            this.Controls.Add(this.btnAddChecklist);
            this.Controls.Add(this.txtSteps);
            this.Controls.Add(this.lsvItems);
            this.Controls.Add(this.lsvMain);
            this.Name = "ChecklistCtl";
            this.Size = new System.Drawing.Size(1337, 800);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnChecklistDown;
        private System.Windows.Forms.Button btnChecklistUp;
        private System.Windows.Forms.Button btnUpdate;
        private System.Windows.Forms.Label lblWorking;
        private System.Windows.Forms.Label lblPass;
        private System.Windows.Forms.Label lblUser;
        private System.Windows.Forms.Label lblTarget;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.Button btnDown;
        private System.Windows.Forms.Button btnUp;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txtChecklistName;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox txtCodeBlock;
        private System.Windows.Forms.TextBox txtEntry;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button btnAddItem;
        private System.Windows.Forms.Button btnAddChecklist;
        private System.Windows.Forms.TextBox txtSteps;
        private System.Windows.Forms.ListView lsvItems;
        private System.Windows.Forms.ListView lsvMain;
    }
}
