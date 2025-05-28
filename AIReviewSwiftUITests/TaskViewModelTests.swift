//
//  TaskViewModelTests.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 26.04.25.
//


import XCTest
@testable import AIReviewSwiftUI

final class TaskViewModelTests: XCTestCase {
    var viewModel: TaskViewModel!

    override func setUp() {
        super.setUp()
        viewModel = TaskViewModel()
    }

    override func tearDown() {
        viewModel = nil
        super.tearDown()
    }

    func testAddTask() {
        XCTAssertTrue(viewModel.tasks.isEmpty)

        viewModel.addTask(title: "New Task")
        XCTAssertEqual(viewModel.tasks.count, 1)
        XCTAssertEqual(viewModel.tasks.first?.title, "New Task")
    }

    func testAddTaskWithEmptyTitle() {
        viewModel.addTask(title: "")
        XCTAssertTrue(viewModel.tasks.isEmpty)
    }

    func testToggleComplete() {
        let task = Task(title: "Test Task")
        viewModel.tasks.append(task)

        viewModel.toggleComplete(task)
        XCTAssertTrue(viewModel.tasks.first?.isCompleted ?? false)

        viewModel.toggleComplete(task)
        XCTAssertFalse(viewModel.tasks.first?.isCompleted ?? true)
    }

    func testCompletedTasks() {
        viewModel.tasks.append(Task(title: "Task 1", isCompleted: true))
        viewModel.tasks.append(Task(title: "Task 2", isCompleted: false))
        viewModel.tasks.append(Task(title: "Task 3", isCompleted: true))

        XCTAssertEqual(viewModel.completedTasks, 2)
    }

    func testOverdueTasks() {
        let pastDate = Calendar.current.date(byAdding: .day, value: -1, to: Date())!
        let futureDate = Calendar.current.date(byAdding: .day, value: 1, to: Date())!

        viewModel.tasks.append(Task(title: "Task 1", dueDate: pastDate))
        viewModel.tasks.append(Task(title: "Task 2", dueDate: futureDate))
        viewModel.tasks.append(Task(title: "Task 3", dueDate: pastDate))

        XCTAssertEqual(viewModel.overdueTasks, 2)
    }
}