const taskListUl = document.getElementById('task-list');
const addTaskForm = document.getElementById('add-task-form');
const taskTitleInput = document.getElementById('task-title');
const taskDescriptionInput = document.getElementById('task-description');
const taskDeadlineInput = document.getElementById('task-deadline');
const addStorageTypeInput = document.getElementById('storage-type');

const filterInput = document.getElementById('filter');
const filterStatusInput = document.getElementById('filter-status');
const filterDeadlineInput = document.getElementById('filter-deadline');
const filterStorageTypeInput = document.getElementById('filter-storage-type');

const findTaskButton = document.getElementById('find-task-button');
const findTaskIdInput = document.getElementById('find-task-id');
const findStorageTypeInput = document.getElementById('find-storage-type');

const deleteTaskButton = document.getElementById('delete-task-button');
const deleteTaskIdInput = document.getElementById('delete-task-id');
const deleteStorageTypeInput = document.getElementById('delete-storage-type');

const updateTaskForm = document.getElementById('update-task-form');
const updateTaskIdInput = document.getElementById('update-task-id');
const updateTitleInput = document.getElementById('update-title');
const updateDescriptionInput = document.getElementById('update-description');
const updateDeadlineInput = document.getElementById('update-deadline');
const updateStatusInput = document.getElementById('update-status');
const updateStorageTypeInput = document.getElementById('update-storage-type');

let tasks = [];

// Function to render tasks
function renderTasks(taskArray) {
    taskListUl.innerHTML = '';
    if (taskArray.length === 0) {
        taskListUl.innerHTML = '<li>No tasks found.</li>';
        return;
    }

    taskArray.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${task.title}</strong> - ${task.description || 'No description'}<br>
            Status: ${task.status} | Deadline: ${task.deadline || 'No deadline'} | Storage: ${task.storage_type} | ID: ${task.id}
        `;
        taskListUl.appendChild(li);
    });
}

// Function to apply filters
function applyFilters() {
    let filteredTasks = tasks;

    const filterText = filterInput.value.toLowerCase();
    if (filterText) {
        filteredTasks = filteredTasks.filter(task =>
            task.title.toLowerCase().includes(filterText) ||
            (task.description && task.description.toLowerCase().includes(filterText))
        );
    }

    const status = filterStatusInput.value;
    if (status) {
        filteredTasks = filteredTasks.filter(task => task.status === status);
    }

    const deadline = filterDeadlineInput.value;
    if (deadline) {
        filteredTasks = filteredTasks.filter(task => {
            if (!task.deadline) return false;
            // Extract only the date part (YYYY-MM-DD) for filtering
            const taskDeadline = task.deadline.split(' ')[0];
            return taskDeadline === deadline;
        });
    }

    const storageType = filterStorageTypeInput.value;
    if (storageType) {
        filteredTasks = filteredTasks.filter(task => task.storage_type === storageType);
    }

    renderTasks(filteredTasks);
}

// Event listeners for filters
filterInput.addEventListener('input', applyFilters);
filterStatusInput.addEventListener('change', applyFilters);
filterDeadlineInput.addEventListener('change', applyFilters);
filterStorageTypeInput.addEventListener('change', applyFilters);

// Function to fetch tasks from the server
async function fetchAndRenderTasks() {
    try {
        const response = await fetch('http://localhost:8000/tasks');
        if (!response.ok) throw new Error('Failed to load tasks');
        tasks = await response.json();
        console.log('Tasks loaded:', tasks);
        applyFilters();
    } catch (error) {
        console.error('Error loading tasks:', error.message, error.stack);
        taskListUl.innerHTML = '<li class="error">Error loading tasks from server.</li>';
    }
}

// Handler for add task form
if (addTaskForm) {
    addTaskForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const title = taskTitleInput.value.trim();
        const description = taskDescriptionInput.value.trim();
        const deadline = taskDeadlineInput.value;
        const storage_type = addStorageTypeInput.value;

        if (!title || !storage_type) {
            alert('Task title and storage type are required.');
            return;
        }

        // Format deadline as "YYYY-MM-DD 23:59:00" (or null if empty)
        let formattedDeadline = null;
        if (deadline) {
            formattedDeadline = `${deadline} 23:59:00`; // Append time to match backend format
        }

        const newTask = {
            title,
            description: description || null,
            deadline: formattedDeadline,
            storage_type
        };

        try {
            // Log the full request details
            console.log('Sending request:', {
                url: 'http://localhost:8000/tasks/add',
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: newTask
            });

            const response = await fetch('http://localhost:8000/tasks/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newTask)
            });

            if (!response.ok) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch (e) {
                    errorData = { detail: 'No response body' };
                }
                throw new Error(`Failed to add task: ${JSON.stringify(errorData)}`);
            }

            const result = await response.json();
            console.log('Task added:', result);
            alert('Task added successfully!');
            addTaskForm.reset();
            fetchAndRenderTasks();
            showSection('list-tasks-section');
        } catch (error) {
            console.error('Error adding task:', error.message, error.stack);
            alert('Error adding task: ' + error.message);
        }
    });
}

// Handler for finding task by ID
if (findTaskButton) {
    findTaskButton.addEventListener('click', async () => {
        const id = findTaskIdInput.value.trim();
        const storage_type = findStorageTypeInput.value;

        if (!id || !storage_type) {
            alert('Task ID and storage type are required.');
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/tasks/${id}?storage_type=${storage_type}`);
            if (!response.ok) throw new Error('Task not found');
            const task = await response.json();
            alert(`Title: ${task.title}\nDescription: ${task.description || 'No description'}\nStatus: ${task.status}\nDeadline: ${task.deadline || 'No deadline'}\nStorage: ${task.storage_type}`);
            findTaskIdInput.value = '';
        } catch (error) {
            console.error('Error finding task:', error.message, error.stack);
            alert('Error: Task not found');
        }
    });
}

// Handler for update task form
if (updateTaskForm) {
    updateTaskForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const id = updateTaskIdInput.value.trim();
        const storage_type = updateStorageTypeInput.value;

        if (!id || !storage_type) {
            alert('Task ID and storage type are required for update.');
            return;
        }

        // Format deadline as "YYYY-MM-DD 23:59:00" (or null if empty)
        let formattedDeadline = null;
        if (updateDeadlineInput.value) {
            formattedDeadline = `${updateDeadlineInput.value} 23:59:00`; // Append time to match backend format
        }

        const updatedTask = {
            title: updateTitleInput.value.trim() || null,
            description: updateDescriptionInput.value.trim() || null,
            deadline: formattedDeadline,
            status: updateStatusInput.value || null,
            storage_type
        };

        if (!updatedTask.title && !updatedTask.description && !updatedTask.deadline && !updatedTask.status) {
            alert('Fill at least one field to update.');
            return;
        }

        try {
            console.log('Updating task:', updatedTask); // Log the request body
            const response = await fetch(`http://localhost:8000/tasks/update/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedTask)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Failed to update task: ${JSON.stringify(errorData)}`);
            }
            const result = await response.json();
            console.log('Task updated:', result);
            alert('Task updated successfully!');
            updateTaskForm.reset();
            fetchAndRenderTasks();
            showSection('list-tasks-section');
        } catch (error) {
            console.error('Error updating task:', error.message, error.stack);
            alert('Error updating task: ' + error.message);
        }
    });
}

// Handler for deleting task
if (deleteTaskButton) {
    deleteTaskButton.addEventListener('click', async () => {
        const id = deleteTaskIdInput.value.trim();
        const storage_type = deleteStorageTypeInput.value;

        if (!id || !storage_type) {
            alert('Task ID and storage type are required for deletion.');
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/tasks/${id}?storage_type=${storage_type}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Failed to delete task: ${JSON.stringify(errorData)}`);
            }
            console.log('Task deleted:', id);
            alert('Task deleted successfully!');
            deleteTaskIdInput.value = '';
            fetchAndRenderTasks();
        } catch (error) {
            console.error('Error deleting task:', error.message, error.stack);
            alert('Error deleting task: ' + error.message);
        }
    });
}

// Function to toggle section visibility
function showSection(sectionId) {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.display = section.id === sectionId ? 'block' : 'none';
    });
}

// Initial load of tasks
fetchAndRenderTasks();