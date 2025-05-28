//
//  ContentView.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 23.04.25.
//

import SwiftUI

/// Main task management view displaying task list and summary
struct ContentView: View {
    @StateObject private var viewModel = TaskViewModel()
    @State private var newTaskTitle = ""

    var body: some View {
        VStack {
            taskInputSection
            taskListSection
            TaskSummaryView(viewModel: viewModel, totalTasks: viewModel.tasks.count, completedTasks: viewModel.completedTasks, overdueTasks: viewModel.overdueTasks)
                .padding(.top)
        }
        .padding()
    }

    private var taskInputSection: some View {
        VStack {
            TextField("Enter task...", text: $newTaskTitle)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button("Add Task") {
                viewModel.addTask(title: newTaskTitle)
                newTaskTitle = ""
            }
            .disabled(newTaskTitle.isEmpty)
        }
    }

    private var taskListSection: some View {
        List {
            ForEach(viewModel.tasks) { task in
                TaskRowView(task: task, onToggle: {
                    viewModel.toggleComplete(task)
                })
            }
        }
    }
}

/// Individual task row displaying task title and completion status
struct TaskRowView: View {
    let task: Task // Assuming Task is your model
    let onToggle: () -> Void

    var body: some View {
        HStack {
            Text(task.title)
            Spacer()
            Button(action: onToggle) {
                Image(systemName: task.isCompleted ? "checkmark.circle.fill" : "circle")
                    .accessibilityLabel(task.isCompleted ? "Mark as incomplete" : "Mark as complete")
            }
        }
    }
}

#Preview {
    ContentView()
}
