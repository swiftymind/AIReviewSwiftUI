//
//  ContentViewTests.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 28.05.25.
//


import Testing
import SwiftUI
import ViewInspector
@testable import AIReviewSwiftUI

extension ContentView: Inspectable {}
extension TaskRowView: Inspectable {}
extension TaskSummaryView: Inspectable {}

struct ContentViewTests {
    @Test func taskInputField_updatesStateOnChange() throws {
        // Arrange
        let contentView = ContentView()
        
        // Act
        try contentView.inspect().find(ViewType.TextField.self).setInput("New Task")
        
        // Assert
        let textValue = try contentView.inspect().find(ViewType.TextField.self).input()
        #expect(textValue == "New Task")
    }
    
    @Test func addTaskButton_isDisabledWhenTextFieldEmpty() throws {
        // Arrange
        let contentView = ContentView()
        
        // Act & Assert
        let button = try contentView.inspect().find(button: "Add Task")
        #expect(try button.isDisabled() == true)
        
        try contentView.inspect().find(ViewType.TextField.self).setInput("New Task")
        #expect(try button.isDisabled() == false)
    }
    
    @Test func taskRowView_displaysCorrectCompletionStatus() throws {
        // Arrange
        let task = Task(id: UUID(), title: "Test Task", isCompleted: false)
        let taskRowView = TaskRowView(task: task, onToggle: {})
        
        // Act & Assert
        let imageName = try taskRowView.inspect().find(ViewType.Image.self).actualImage().name
        #expect(imageName == "circle")
        
        let completedTask = Task(id: UUID(), title: "Test Task", isCompleted: true)
        let completedTaskRowView = TaskRowView(task: completedTask, onToggle: {})
        let completedImageName = try completedTaskRowView.inspect().find(ViewType.Image.self).actualImage().name
        #expect(completedImageName == "checkmark.circle.fill")
    }
}
