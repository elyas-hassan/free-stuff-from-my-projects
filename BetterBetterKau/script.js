
let gridStartHour = 8;
let gridEndHour = 17;
const HOUR_HEIGHT = 100;
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu'];

const predefinedSchedules = {
    'CS1': [
        { name: "CPCS324 (Lec)", days: ["Sun", "Tue", "Thu"], start: "10:00", end: "10:50", type: "lec" },
        { name: "CPCS324 (Lab)", days: ["Wed"], start: "11:00", end: "12:40", type: "lab" },
        { name: "CPCS331 (Lec)", days: ["Sun", "Tue", "Thu"], start: "09:00", end: "09:50", type: "lec" },
        { name: "CPCS331 (Lab)", days: ["Wed"], start: "09:10", end: "10:50", type: "lab" },
        { name: "CPCS351 (Lec)", days: ["Sun", "Tue", "Thu"], start: "11:00", end: "11:50", type: "lec" },
        { name: "CPCS351 (Lab)", days: ["Wed"], start: "12:50", end: "14:30", type: "lab" },
        { name: "CPCS361 (Lec)", days: ["Sun", "Tue", "Thu"], start: "13:00", end: "13:50", type: "lec" },
        { name: "CPCS361 (Lab)", days: ["Wed"], start: "18:20", end: "20:00", type: "lab" },
        { name: "CPCS371 (Lec)", days: ["Sun", "Tue", "Thu"], start: "14:00", end: "14:50", type: "lec" },
        { name: "CPCS371 (Lab)", days: ["Wed"], start: "16:30", end: "18:10", type: "lab" },
        { name: "CPIS334 (Lec)", days: ["Sun", "Tue"], start: "15:00", end: "15:50", type: "lec" },
        { name: "CPIS334 (Lab)", days: ["Thu"], start: "15:00", end: "16:40", type: "lab" }
    ],
    'CS2': [
        { name: "CPCS324 (Lec)", days: ["Sun", "Tue", "Thu"], start: "11:00", end: "11:50", type: "lec" },
        { name: "CPCS324 (Lab)", days: ["Wed"], start: "12:50", end: "14:30", type: "lab" },
        { name: "CPCS331 (Lec)", days: ["Sun", "Tue", "Thu"], start: "10:00", end: "10:50", type: "lec" },
        { name: "CPCS331 (Lab)", days: ["Wed"], start: "11:00", end: "12:40", type: "lab" },
        { name: "CPCS351 (Lec)", days: ["Sun", "Tue", "Thu"], start: "09:00", end: "09:50", type: "lec" },
        { name: "CPCS351 (Lab)", days: ["Wed"], start: "09:10", end: "10:50", type: "lab" },
        { name: "CPCS361 (Lec)", days: ["Sun", "Tue", "Thu"], start: "14:00", end: "14:50", type: "lec" },
        { name: "CPCS361 (Lab)", days: ["Wed"], start: "16:30", end: "18:10", type: "lab" },
        { name: "CPCS371 (Lec)", days: ["Sun", "Tue", "Thu"], start: "13:00", end: "13:50", type: "lec" },
        { name: "CPCS371 (Lab)", days: ["Wed"], start: "14:40", end: "16:20", type: "lab" },
        { name: "CPIS334 (Lec)", days: ["Sun", "Tue"], start: "16:00", end: "16:50", type: "lec" },
        { name: "CPIS334 (Lab)", days: ["Thu"], start: "17:00", end: "18:40", type: "lab" }
    ],
    'CS3': [
        { name: "CPCS324 (Lec)", days: ["Sun", "Tue", "Thu"], start: "13:00", end: "13:50", type: "lec" },
        { name: "CPCS324 (Lab)", days: ["Wed"], start: "09:10", end: "10:50", type: "lab" },
        { name: "CPCS331 (Lec)", days: ["Sun", "Tue", "Thu"], start: "14:00", end: "14:50", type: "lec" },
        { name: "CPCS331 (Lab)", days: ["Wed"], start: "12:50", end: "14:30", type: "lab" },
        { name: "CPCS351 (Lec)", days: ["Sun", "Tue", "Thu"], start: "10:00", end: "10:50", type: "lec" },
        { name: "CPCS351 (Lab)", days: ["Wed"], start: "11:00", end: "12:40", type: "lab" },
        { name: "CPCS361 (Lec)", days: ["Sun", "Tue", "Thu"], start: "09:00", end: "09:50", type: "lec" },
        { name: "CPCS361 (Lab)", days: ["Mon"], start: "12:50", end: "14:30", type: "lab" },
        { name: "CPCS371 (Lec)", days: ["Sun", "Tue", "Thu"], start: "11:00", end: "11:50", type: "lec" },
        { name: "CPCS371 (Lab)", days: ["Mon"], start: "14:40", end: "16:20", type: "lab" },
        { name: "CPIS334 (Lec)", days: ["Sun", "Tue"], start: "18:00", end: "18:50", type: "lec" },
        { name: "CPIS334 (Lab)", days: ["Wed"], start: "16:30", end: "18:10", type: "lab" }
    ]
};


let availableCourses = [];
let selectedCourseData = null;
let currentSchedule = [];

document.addEventListener('DOMContentLoaded', () => {
    loadCourseList();
    loadScheduleLocally();
    setupThemeSwitcher(); 
    setupPrebuiltScheduleLoader();
    
});



function updateGridBounds() {
    if (currentSchedule.length === 0) {

        gridStartHour = 8;
        gridEndHour = 17;
    } else {
        let minMin = 24 * 60; 
        let maxMin = 0;       

        currentSchedule.forEach(event => {
            
            const [startStr, endStr] = event.timeRange.split(' - ');
            const s = parseTimeToMinutes(startStr);
            const e = parseTimeToMinutes(endStr);
            if (s < minMin) minMin = s;
            if (e > maxMin) maxMin = e;
        });

        
        gridStartHour = Math.floor(minMin / 60);
        gridEndHour = Math.ceil(maxMin / 60);

        
    }

    
    initGrid();
}

function initGrid() {
    const timeCol = document.getElementById('timeMarkers');
    timeCol.innerHTML = ''; 

    const totalHours = gridEndHour - gridStartHour;

    
    document.querySelectorAll('.day-column, .time-column').forEach(el => {
        el.style.height = `${totalHours * HOUR_HEIGHT}px`;
        if(el.classList.contains('day-column')) {
            el.style.backgroundSize = `100% ${HOUR_HEIGHT}px`;
        }
    });

    
    for (let i = 0; i < totalHours; i++) {
        const div = document.createElement('div');
        div.className = 'time-marker';
        div.style.height = `${HOUR_HEIGHT}px`;
        const hour = gridStartHour + i;
        const period = hour >= 12 ? 'PM' : 'AM';
        const displayHour = hour > 12 ? hour - 12 : hour;
    
        const niceHour = (hour === 0 || hour === 24) ? 12 : displayHour;

        div.textContent = `${niceHour}:00 ${period}`;
        timeCol.appendChild(div);
    }
}

function renderAllEvents() {
    
    document.querySelectorAll('.schedule-event').forEach(el => el.remove());

    
    currentSchedule.forEach(event => renderEvent(event));
}

function parseTimeToMinutes(timeStr) {
    const [time, period] = timeStr.split(' ');
    let [hours, minutes] = time.split(':').map(Number);
    if (period === 'PM' && hours !== 12) hours += 12;
    if (period === 'AM' && hours === 12) hours = 0;
    return (hours * 60) + minutes;
}


async function loadCourseList() {

    const courseFiles = [
        'ASTR201.json',
        'CPCS211.json',
        'CPCS223.json',
        'CPCS241.json'
    ];

    for (const file of courseFiles) {
        try {
            const response = await fetch(`courses/${file}`);
            const data = await response.json();
            availableCourses.push(data);
        } catch (error) {
            console.error("Error loading course:", file, error);
        }
    }

    
    const savedCustomCourses = JSON.parse(localStorage.getItem('customCourses')) || [];
    savedCustomCourses.forEach(customCourse => {
    
        const courseData = {
            courseCode: customCourse.name,
            name: `(Custom Event)`,
            hours: 0,
            isCustom: true,
            sections: [{
                section: customCourse.section || '',
                lecture: { days: customCourse.days, time: customCourse.time, instructor: customCourse.instructor || '' }
            }]
        };
        availableCourses.push(courseData);
    });

    renderDropdownOptions(availableCourses);
}


function toggleDropdown() {
    const menu = document.getElementById('dropdownMenu');
    const input = document.querySelector('.dropdown-search');

    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
        input.value = '';
        renderDropdownOptions(availableCourses);
    }
}

function filterCourses() {
    const input = document.querySelector('.dropdown-search').value.toLowerCase();
    const filtered = availableCourses.filter(c =>
        c.courseCode.toLowerCase().includes(input) ||
        c.name.toLowerCase().includes(input)
    );
    renderDropdownOptions(filtered);
}

function renderDropdownOptions(courses) {
    const container = document.getElementById('courseOptions');
    container.innerHTML = '';
    courses.forEach(course => {
        const div = document.createElement('div');
        div.className = 'dropdown-option';
        if (course.isCustom) {
            div.innerHTML = `<strong>${course.courseCode}</strong> <span style="color: #aaa; font-style: italic;">- Custom</span>`;
        } else {
            div.innerHTML = `<strong>${course.courseCode}</strong> - ${course.name}`;
        }
        div.onclick = () => selectCourse(course);
        container.appendChild(div);
    });
    if(courses.length > 0 && container.innerHTML !== '') {
         
    }
}

function selectCourse(course) {
    document.querySelector('.dropdown-text').textContent = `${course.courseCode}`;
    document.getElementById('dropdownMenu').style.display = 'none';
    selectedCourseData = course;

    const select = document.getElementById('sectionSelect');
    select.innerHTML = '<option value="">Select a Section...</option>';
    select.disabled = false;

    if (course.isCustom) {
        
        const opt = document.createElement('option');
        opt.value = 0;
        opt.textContent = `Default`;
        select.appendChild(opt);
        select.value = 0;
    } else {
        course.sections.forEach((sec, index) => {
            const opt = document.createElement('option');
            opt.value = index;
            opt.textContent = `Section ${sec.section} (CRN: ${sec.crn})`;
            select.appendChild(opt);
        });
    }
    document.getElementById('addBtn').disabled = true;
}

function handleSectionSelect() {
    document.getElementById('addBtn').disabled = false;
}

function addCourseToSchedule() {
    const sectionIndex = document.getElementById('sectionSelect').value;
    if (!selectedCourseData || sectionIndex === "") return;

    const section = selectedCourseData.sections[sectionIndex];

    const isLightTheme = document.body.classList.contains('light-theme');
    const hue = Math.floor(Math.random() * 360);
    const saturation = isLightTheme ? '65%' : '70%';
    const lightness = isLightTheme ? '88%' : '35%';
    const color = `hsl(${hue}, ${saturation}, ${lightness})`;

    const groupId = "group_" + Date.now() + "_" + Math.floor(Math.random() * 1000);

    if (section.lecture) processTimeBlock(section.lecture, selectedCourseData, section.section, 'Lecture', color, groupId);
    if (section.lab && section.lab.time !== "TBA") processTimeBlock(section.lab, selectedCourseData, section.section, 'Lab', color, groupId);

    updateTotalHours(selectedCourseData.hours);

    updateGridBounds();
    renderAllEvents();
    saveScheduleLocally();
}

function processTimeBlock(timeObj, courseData, sectionCode, type, color, groupId) {
    if (!timeObj.time || timeObj.time === "TBA") return;

    timeObj.days.forEach(day => {
        const event = {
            id: Date.now() + Math.random(),
            groupId: groupId,
            day: day,
            color,
            code: courseData.courseCode,
            section: sectionCode,
            instructor: timeObj.instructor || '',
            timeRange: timeObj.time,
            hours: courseData.hours
        };
        currentSchedule.push(event);
    });
}

function renderEvent(event) {
    const col = document.querySelector(`.day-column[data-day="${event.day}"]`);
    if (!col) return;

    const [startStr, endStr] = event.timeRange.split(' - ');
    const startMin = parseTimeToMinutes(startStr);
    const endMin = parseTimeToMinutes(endStr);

    const scheduleStartMin = gridStartHour * 60;

    const top = ((startMin - scheduleStartMin) / 60) * HOUR_HEIGHT;
    const height = ((endMin - startMin) / 60) * HOUR_HEIGHT;

    const el = document.createElement('div');
    el.className = 'schedule-event';
    el.setAttribute('data-group-id', event.groupId);
    el.style.top = `${top}px`;
    el.style.height = `${height}px`;
    el.style.backgroundColor = event.color;

    el.innerHTML = `
        <div class="event-controls">
            <input type="color" class="color-input" value="${rgbToHex(event.color)}"
                   onchange="updateGroupColor('${event.groupId}', this.value)">
            <button class="remove-event" onclick="deleteCourseGroup('${event.groupId}')">×</button>
        </div>
        
        <span class="event-course-code">${event.code}</span>
        <div class="event-details">
            <span class="event-section-code">${event.section}</span>
            <span class="event-time" style="font-weight:bold; color:#fff;">${event.timeRange}</span>
            <span class="event-time" style="opacity:0.8;">${event.instructor}</span>
        </div>
    `;
    col.appendChild(el);
}


function deleteCourseGroup(groupId) {
    const idString = String(groupId);

    const representative = currentSchedule.find(e => String(e.groupId) === idString);

    if (representative && representative.hours) {
        updateTotalHours(-representative.hours);
    } else {
        console.warn("Could not find course with ID:", idString);
    }

    currentSchedule = currentSchedule.filter(e => String(e.groupId) !== idString);

    updateGridBounds();
    renderAllEvents();
    saveScheduleLocally();
}

function updateGroupColor(groupId, newColor) {
    const idString = String(groupId);

    currentSchedule.forEach(e => {
        if(String(e.groupId) === idString) e.color = newColor;
    });

    document.querySelectorAll(`.schedule-event[data-group-id="${idString}"]`).forEach(el => {
        el.style.backgroundColor = newColor;
    });

    document.querySelectorAll(`.schedule-event[data-group-id="${idString}"] .color-input`).forEach(input => {
        input.value = newColor;
    });

    saveScheduleLocally();
}

function saveScheduleLocally() {
    const dataToSave = {
        schedule: currentSchedule,
        totalHours: document.getElementById('totalHours').textContent
    };
    localStorage.setItem('studentScheduleData', JSON.stringify(dataToSave));
}

function loadScheduleLocally() {
    const saved = localStorage.getItem('studentScheduleData');
    if (saved) {
        const data = JSON.parse(saved);
        currentSchedule = data.schedule || [];
        document.getElementById('totalHours').textContent = data.totalHours || '0';
    }
    updateGridBounds();
    renderAllEvents();
}

function addCustomCourse() {
    const name = document.getElementById('customName').value;
    const sectionVal = document.getElementById('customSection').value;
    const instructorVal = document.getElementById('customInstructor').value;
    const start = document.getElementById('customStart').value;
    const end = document.getElementById('customEnd').value;
    const checkboxes = document.querySelectorAll('.day-checkboxes input:checked');

    if(!name || !start || !end || checkboxes.length === 0) {
        alert('Please fill in Course Name, Time, and select at least one Day.');
        return;
    }

    const savedCustomCourses = JSON.parse(localStorage.getItem('customCourses')) || [];
    const newCustomEvent = {
        name: name,
        section: sectionVal,
        instructor: instructorVal,
        time: `${start} - ${end}`,
        days: Array.from(checkboxes).map(cb => cb.value)
    };

    if (!savedCustomCourses.some(c => c.name === newCustomEvent.name)) {
        savedCustomCourses.push(newCustomEvent);
        localStorage.setItem('customCourses', JSON.stringify(savedCustomCourses));
    }

    const formatTime = (t) => {
        let [h, m] = t.split(':').map(Number);
        const p = h >= 12 ? 'PM' : 'AM';
        if(h > 12) h -= 12; if(h === 0) h = 12;
        return `${h}:${m} ${p}`;
    };

    const timeStr = `${formatTime(start)} - ${formatTime(end)}`;
    const days = Array.from(checkboxes).map(cb => cb.value);

    const groupId = "custom_" + Date.now();
    const color = '#6c757d';

    const customSection = {
        time: timeStr,
        days: days,
        instructor: instructorVal || ''
    };

    processTimeBlock(
        customSection,
        { courseCode: name, hours: 0 },
        sectionVal || '',
        'Event',
        color,
        groupId
    );

    updateGridBounds();
    renderAllEvents();
    saveScheduleLocally();
    closeModal();

    document.getElementById('customName').value = '';
    document.getElementById('customSection').value = '';
    document.getElementById('customInstructor').value = '';
    checkboxes.forEach(cb => cb.checked = false);

    loadCourseList();
}

function updateTotalHours(hours) {
    const el = document.getElementById('totalHours');
    el.textContent = parseInt(el.textContent) + hours;
}

function clearSchedule() {
    currentSchedule = [];
    document.getElementById('totalHours').textContent = '0';
    localStorage.removeItem('studentScheduleData');
    
    updateGridBounds();
    renderAllEvents();
}

function downloadSchedule() {
    const element = document.getElementById("scheduleGrid");
    const controls = document.querySelectorAll('.event-controls');

    controls.forEach(controlDiv => { controlDiv.style.display = 'none'; });

    html2canvas(element, {
        backgroundColor: "#f8f9fa",
        scale: 2
    }).then(canvas => {
        controls.forEach(controlDiv => { controlDiv.style.display = ''; });
        const link = document.createElement('a');
        link.download = 'schedule.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}

function rgbToHex(color) {
    if(color.startsWith('#')) return color;
    const div = document.createElement('div');
    div.style.color = color;
    document.body.appendChild(div);
    const computed = window.getComputedStyle(div).color;
    document.body.removeChild(div);
    const rgb = computed.match(/\d+/g);
    if(!rgb) return '#000000';
    return "#" + ((1 << 24) + (parseInt(rgb[0]) << 16) + (parseInt(rgb[1]) << 8) + parseInt(rgb[2])).toString(16).slice(1);
}

function setupPrebuiltScheduleLoader() {
    const container = document.getElementById('prebuilt-loader-container');
    if (!container) return;

    container.innerHTML = `
        <label>Or Load a Pre-built Schedule:</label>
        <div class="custom-dropdown" id="prebuiltDropdown">
            <div class="dropdown-toggle" onclick="togglePrebuiltDropdown()">
                <span class="dropdown-text">Select a plan...</span>
                <span class="dropdown-arrow">▼</span>
            </div>
            <div class="dropdown-menu" id="prebuiltDropdownMenu" style="display: none;">
                <div class="dropdown-options" id="prebuiltOptions"></div>
            </div>
        </div>
    `;

    const optionsContainer = document.getElementById('prebuiltOptions');

    Object.keys(predefinedSchedules).forEach(key => {
        const div = document.createElement('div');
        div.className = 'dropdown-option';
        div.textContent = `Load Plan: ${key}`;
        div.onclick = () => loadPrebuiltSchedule(key);
        optionsContainer.appendChild(div);
    });
}

function togglePrebuiltDropdown() {
    const menu = document.getElementById('prebuiltDropdownMenu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

function loadPrebuiltSchedule(selectedKey) {
    const menu = document.getElementById('prebuiltDropdownMenu');
    menu.style.display = 'none';

    const confirmation = confirm(`This will clear your current schedule and load the "${selectedKey}" plan. Are you sure?`);
    if (confirmation) {
        const scheduleData = predefinedSchedules[selectedKey];
        if (!scheduleData) return;

        clearSchedule();

        const groupedCourses = scheduleData.reduce((acc, item) => {
            const courseName = item.name.split(' (')[0];
            if (!acc[courseName]) {
                acc[courseName] = [];
            }
            acc[courseName].push(item);
            return acc;
        }, {});

        Object.values(groupedCourses).forEach(courseGroup => {
            const isLightTheme = document.body.classList.contains('light-theme');
            const hue = Math.floor(Math.random() * 360);
            const saturation = isLightTheme ? '65%' : '80%';
            const lightness = isLightTheme ? '88%' : '35%';
            const color = `hsl(${hue}, ${saturation}, ${lightness})`;
            const groupId = "group_" + Date.now() + "_" + Math.random();

            courseGroup.forEach(item => {
                const timeRange = `${item.start} - ${item.end}`.replace(/(\d{2}:\d{2})/g, t => {
                    let [h, m] = t.split(':');
                    const p = h >= 12 ? 'PM' : 'AM';
                    if (h > 12) h -= 12; if (h == 0) h = 12;
                    return `${parseInt(h)}:${m} ${p}`;
                }).replace(' 00','');
                processTimeBlock({ time: timeRange, days: item.days }, { courseCode: item.name, hours: 0 }, '', item.type, color, groupId);
            });
        });

        updateGridBounds();
        renderAllEvents();
        saveScheduleLocally();
    }
}

function setupThemeSwitcher() {
    const themeToggleBtn = document.getElementById('themeToggle');

    const currentTheme = localStorage.getItem('theme') || 'dark';
    setTheme(currentTheme);

    themeToggleBtn.addEventListener('click', () => {
        let newTheme = document.body.classList.contains('light-theme') ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });

    function setTheme(theme) {
        if (theme === 'light') {
            document.body.classList.add('light-theme');
            themeToggleBtn.innerHTML = `🌙 Dark Mode`;
        } else {
            document.body.classList.remove('light-theme');
            themeToggleBtn.innerHTML = `☀️ Light Mode`;
        }
    }
}

function openModal() { document.getElementById('customModal').style.display = 'flex'; }
function closeModal() { document.getElementById('customModal').style.display = 'none'; }
window.onclick = function(e) {
    const m = document.getElementById('customModal');
    if (e.target == m) m.style.display = "none";
}
