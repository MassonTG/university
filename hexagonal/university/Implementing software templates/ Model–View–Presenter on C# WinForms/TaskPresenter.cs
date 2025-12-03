using System.Collections.Generic;

namespace MVP_ToDoList
{
    public class TaskPresenter
    {
        private List<TaskModel> tasks;
        private ITaskView view;

        public TaskPresenter(ITaskView v)
        {
            tasks = new List<TaskModel>();
            view = v;
        }

        public void AddTask(string description)
        {
            tasks.Add(new TaskModel { Description = description, IsDone = false });
            view.ShowTasks(tasks);
        }

        public void ToggleTask(int index)
        {
            tasks[index].IsDone = !tasks[index].IsDone;
            view.ShowTasks(tasks);
        }
    }
}
