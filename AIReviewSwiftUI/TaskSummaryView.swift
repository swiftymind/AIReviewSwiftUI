//
//  TaskSummaryView.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 26.04.25.
//


import SwiftUI

struct TaskSummaryView: View {
    @ObservedObject var viewModel: TaskViewModel
    var totalTasks: Int
    var completedTasks: Int
    var overdueTasks: Int
    var body: some View {
        VStack {
            Text("Task Summary")
                .font(.headline)
                .padding()

            HStack {
                Text("Total Tasks: \(viewModel.tasks.count)")
                Spacer()
                Text("Completed Tasks: \(viewModel.completedTasks)")
            }
            .padding()
        }
        .padding()
    }
}

#Preview {
    TaskSummaryView(viewModel: TaskViewModel(), totalTasks: 0, completedTasks: 0, overdueTasks: 0)
}
