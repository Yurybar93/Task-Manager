const taskListUl = document.getElementById('task-list');
const addTaskForm = document.getElementById('add-task-form');
const taskTitleInput = document.getElementById('task-title');
const taskDescriptionInput = document.getElementById('task-description');
const taskDeadlineInput = document.getElementById('task-deadline');
const addStorageTypeInput = document.getElementById('storage-type');

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

const exportTaskForm = document.getElementById('export-task-form');
const exportFilenameInput = document.getElementById('export-filename');
const exportFormatInput = document.getElementById('export-format');
const exportStorageTypeInput = document.getElementById('export-storage-type');

let tasks = [];

// Function to render tasks
function renderTasks(taskArray) {
    taskListUl.innerHTML = '';
    console.log('Rendering tasks:', taskArray); // Debug log
    if (taskArray.length === 0) {
        taskListUl.innerHTML = '<li>No tasks found.</li>';
        return;
    }

    taskArray.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${task.title}</strong> - ${task.description || 'No description'}<br>
            Status: ${task.status} | Deadline: ${task.deadline || 'No deadline'} | Storage: ${filterStorageTypeInput.value || 'undefined'} | ID: ${task.id}
        `;
        taskListUl.appendChild(li);
    });
}

// Function to apply filters
function applyFilters() {
    let filteredTasks = tasks;

    // Log filter values for debugging
    console.log('Filter values:', {
        status: filterStatusInput.value,
        deadline: filterDeadlineInput.value,
        storageType: filterStorageTypeInput.value
    });

    const status = filterStatusInput.value;
    if (status) {
        filteredTasks = filteredTasks.filter(task => 
            task.status && task.status.toLowerCase() === status.toLowerCase()
        );
    }

    const deadline = filterDeadlineInput.value;
    if (deadline) {
        filteredTasks = filteredTasks.filter(task => {
            if (!task.deadline) return false;
            const taskDeadline = task.deadline.split('T')[0];
            return taskDeadline === deadline;
        });
    }

    console.log('Filtered tasks:', filteredTasks);
    renderTasks(filteredTasks);
}

// Event listeners for filters
filterStatusInput.addEventListener('change', applyFilters);
filterDeadlineInput.addEventListener('change', applyFilters);
filterStorageTypeInput.addEventListener('change', () => {
    console.log('Storage type filter changed to:', filterStorageTypeInput.value);
    fetchAndRenderTasks();
});

// Function to fetch tasks from the server
async function fetchAndRenderTasks() {
    try {
        const storageType = filterStorageTypeInput.value;
        const url = storageType
            ? `http://localhost:8000/tasks?storage_type=${storageType}`
            : 'http://localhost:8000/tasks';
        
        console.log('Fetching tasks from:', url);
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`Failed to load tasks: ${JSON.stringify(errorData)} (Status: ${response.status})`);
        }

        const data = await response.json();
        tasks = Array.isArray(data) ? data : [];
        console.log('Raw tasks data:', data);
        console.log('Tasks loaded:', tasks);
        applyFilters();
    } catch (error) {
        console.error('Error loading tasks:', error.message, error.stack);
        taskListUl.innerHTML = '<li class="error">Error loading tasks from server: ' + error.message + '</li>';
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

        let formattedDeadline = null;
        if (deadline) {
            formattedDeadline = `${deadline} 23:59:00`; // Формат "YYYY-MM-DD HH:mm:ss"
        }

        const newTask = {
            title,
            description: description || null,
            deadline: formattedDeadline,
            status: "pending", // Добавляем статус по умолчанию
            storage_type
        };

        try {
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
            alert(`Title: ${task.title}\nDescription: ${task.description || 'No description'}\nStatus: ${task.status}\nDeadline: ${task.deadline || 'No deadline'}\nStorage: ${storage_type}`);
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

        let formattedDeadline = null;
        if (updateDeadlineInput.value) {
            formattedDeadline = `${updateDeadlineInput.value} 23:59:00`; // Формат "YYYY-MM-DD HH:mm:ss"
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
            console.log('Updating task:', updatedTask);
            const url = `http://localhost:8000/tasks/update/${id}?storage_type=${storage_type}`;
            console.log('Sending update request to:', url);
            const response = await fetch(url, {
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

// Handler for export task form
if (exportTaskForm) {
    exportTaskForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const filename = exportFilenameInput.value.trim();
        const format = exportFormatInput.value;
        const storage_type = exportStorageTypeInput.value || 'jsonfile'; // Значение по умолчанию из config

        if (!filename || !format) {
            alert('File name and format are required.');
            return;
        }

        try {
            const url = `http://localhost:8000/tasks/export?filename=${encodeURIComponent(filename)}&format=${format}&storage_type=${storage_type}`;
            console.log('Exporting tasks from:', url);
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/octet-stream' // Ожидаем файл
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Failed to export tasks: ${JSON.stringify(errorData)}`);
            }

            // Получаем данные и создаем ссылку для скачивания
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `${filename}.${format}`; // Имя файла с расширением
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);
            alert('Tasks exported successfully!');
        } catch (error) {
            console.error('Error exporting tasks:', error.message, error.stack);
            alert('Error exporting tasks: ' + error.message);
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