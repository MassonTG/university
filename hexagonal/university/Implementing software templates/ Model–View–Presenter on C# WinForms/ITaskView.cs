using System.Collections.Generic;

namespace MVP_ToDoList
{
    public interface ITaskView
    {
        void ShowTasks(List<TaskModel> tasks);
    }
}
