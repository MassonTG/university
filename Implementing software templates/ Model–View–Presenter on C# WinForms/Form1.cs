using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace MVP_ToDoList
{
    public partial class Form1 : Form, ITaskView
    {
        private TaskPresenter presenter;

        public Form1()
        {
            InitializeComponent();
            presenter = new TaskPresenter(this);
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            presenter.AddTask(txtTask.Text);
            txtTask.Clear();
        }

        public void ShowTasks(List<TaskModel> tasks)
        {
            listBoxTasks.Items.Clear();
            foreach (var t in tasks)
            {
                string status = t.IsDone ? "[✔]" : "[ ]";
                listBoxTasks.Items.Add($"{status} {t.Description}");
            }
        }

        private void listBoxTasks_DoubleClick(object sender, EventArgs e)
        {
            if (listBoxTasks.SelectedIndex >= 0)
                presenter.ToggleTask(listBoxTasks.SelectedIndex);
        }
    }
}
