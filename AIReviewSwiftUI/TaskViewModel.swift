//
//  TaskViewModel.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 23.04.25.
//


import Foundation

final class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = []


    func addTask(title: String) {
        guard !title.isEmpty else { return }
        tasks.append(Task(title: title))
    }
    
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
