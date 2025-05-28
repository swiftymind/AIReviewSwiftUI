//
//  Task.swift
//  AIReviewSwiftUI
//
//  Created by kanagasabapathy on 23.04.25.
//

import Foundation

/// `Task` represents a single to-do item in the application
///
/// 
/// This struct conforms to the Identifiable protocol to enable easy integration with SwiftUI lists
struct Task: Identifiable {
    let id = UUID()
    var title: String
    var isCompleted: Bool = false
    var dueDate: Date? = nil
}

