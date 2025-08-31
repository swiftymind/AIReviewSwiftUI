//
//  TaskViewModel.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 23.04.25.
//


import Foundation

final class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = []


    /// Adds a new task with the specified title to the task list if the title is not empty.
    ///
    /// - Parameter title: The title for the new task. If empty, no task is added.
    func addTask(title: String) {
        guard !title.isEmpty else { return }
        tasks.append(Task(title: title))
    }
    
    /// Toggles the completion status of the specified task if it exists in the tasks array.
    ///
    /// If the task is found by its identifier, its `isCompleted` property is flipped. If not found, no action is taken.
    func toggleComplete(_ task: Task) {
        guard let index = tasks.firstIndex(where: { $0.id == task.id }) else { return }
        tasks[index].isCompleted.toggle()
    }

    

    var completedTasks: Int {
        tasks.filter { $0.isCompleted }.count
    }
    var overdueTasks: Int {
        tasks.filter { $0.dueDate != nil && $0.dueDate! < Date() }.count
    }
}
