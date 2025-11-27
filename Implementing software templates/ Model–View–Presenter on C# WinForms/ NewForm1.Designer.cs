namespace MVP_ToDoList
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.TextBox txtTask;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.ListBox listBoxTasks;

        private void InitializeComponent()
        {
            this.txtTask = new System.Windows.Forms.TextBox();
            this.btnAdd = new System.Windows.Forms.Button();
            this.listBoxTasks = new System.Windows.Forms.ListBox();
            this.SuspendLayout();
            // 
            // txtTask
            // 
            this.txtTask.Location = new System.Drawing.Point(12, 12);
            this.txtTask.Size = new System.Drawing.Size(200, 20);
            // 
            // btnAdd
            // 
            this.btnAdd.Location = new System.Drawing.Point(220, 10);
            this.btnAdd.Size = new System.Drawing.Size(75, 23);
            this.btnAdd.Text = "Add";
            this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
            // 
            // listBoxTasks
            // 
            this.listBoxTasks.Location = new System.Drawing.Point(12, 40);
            this.listBoxTasks.Size = new System.Drawing.Size(280, 200);
            this.listBoxTasks.DoubleClick += new System.EventHandler(this.listBoxTasks_DoubleClick);
            // 
            // Form1
            // 
            this.ClientSize = new System.Drawing.Size(304, 261);
            this.Controls.Add(this.txtTask);
            this.Controls.Add(this.btnAdd);
            this.Controls.Add(this.listBoxTasks);
            this.Text = "MVP To-Do List";
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
