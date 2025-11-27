using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace MVC_ToDoList
{
    // -------- Model -------
    public class TaskModel
    {
        public string Description { get; set; }
        public bool IsDone { get; set; }
    }

    // ---- Controller -------
    public class TaskController
    {
        private List<TaskModel> tasks;
        private Form1 view;

        public TaskController(Form1 v)
        {
            tasks = new List<TaskModel>();
            view = v;
        }

        public void AddTask(string description)
        {
            tasks.Add(new TaskModel { Description = description, IsDone = false });
            UpdateView();
        }

        public void ToggleTask(int index)
        {
            tasks[index].IsDone = !tasks[index].IsDone;
            UpdateView();
        }

        private void UpdateView()
        {
            view.UpdateTaskList(tasks);
        }
    }

    // -------- View ---------
    public partial class Form1 : Form
    {
        private TaskController controller;

        public Form1()
        {
            InitializeComponent();
            controller = new TaskController(this);
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            controller.AddTask(txtTask.Text);
            txtTask.Clear();
        }

        public void UpdateTaskList(List<TaskModel> tasks)
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
                controller.ToggleTask(listBoxTasks.SelectedIndex);
        }
    }
}
