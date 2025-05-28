//
//  TaskSummaryViewTests.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 28.05.25.
//


import Testing
import SwiftUI
import ViewInspector
@testable import AIReviewSwiftUI

struct TaskSummaryViewTests {
    @Test func taskSummaryView_displaysCorrectCounts() throws {
        // Arrange
        let viewModel = TaskViewModel()
        viewModel.addTask(title: "Task 1")
        viewModel.addTask(title: "Task 2")
        
        if let task = viewModel.tasks.first {
            viewModel.toggleComplete(task)
        }
        
        // Act
        let summaryView = TaskSummaryView(viewModel: viewModel)
        
        // Assert
        let text = try summaryView.inspect().find(ViewType.Text.self).string()
        #expect(text.contains("Total: 2"))
        #expect(text.contains("Completed: 1"))
    }
}
