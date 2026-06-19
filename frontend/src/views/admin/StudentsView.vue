<template>
  <DashboardLayout>
    <PageHeader
      title="Students"
      subtitle="Manage student accounts, status, and records."
    >
      <template #actions>
        <button type="button" class="btn btn-primary">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="icon icon-tabler icons-tabler-outline icon-tabler-download"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
            <path d="M7 11l5 5l5 -5" />
            <path d="M12 4l0 12" />
          </svg>
          Export
        </button>
      </template>
    </PageHeader>

    <div class="row g-4 mb-4">
      <div class="col-md-3">
        <StatCard title="Students" :value="totalStudents" />
      </div>

      <div class="col-md-3">
        <StatCard title="Active" :value="activeStudents" />
      </div>

      <div class="col-md-3">
        <StatCard title="Inactive" :value="inactiveStudents" />
      </div>

      <div class="col-md-3">
        <StatCard title="Blacklisted" :value="blacklistedStudents" />
      </div>
    </div>

    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-lg-6">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search by name, roll number, or department..."
            />
          </div>

          <div class="col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="blacklisted">Blacklisted</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <DataTable title="Students" :headers="headers" :rows="filteredStudents">
      <template #status="{ row }">
        <span
          class="badge"
          :class="{
            'bg-success': row.status === 'Active',
            'bg-warning text-dark': row.status === 'Inactive',
            'bg-danger': row.status === 'Blacklisted',
          }"
        >
          {{ row.status }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="btn-group btn-group-sm">
          <button class="btn btn-outline-primary" @click="viewStudent(row)">
            View
          </button>

          <button
            v-if="row.status === 'Active'"
            class="btn btn-outline-warning"
            @click="confirmDeactivate(row)"
          >
            Deactivate
          </button>

          <button
            v-if="row.status === 'Inactive'"
            class="btn btn-outline-success"
            @click="activateStudent(row)"
          >
            Activate
          </button>

          <button
            v-if="row.status === 'Blacklisted'"
            class="btn btn-outline-success"
            @click="restoreStudent(row)"
          >
            Restore
          </button>

          <button
            class="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split"
            data-bs-toggle="dropdown"
          ></button>

          <ul class="dropdown-menu dropdown-menu-end">
            <li v-if="row.status !== 'Blacklisted'">
              <a
                class="dropdown-item text-danger"
                href="#"
                @click.prevent="confirmBlacklist(row)"
              >
                Blacklist
              </a>
            </li>
          </ul>
        </div>
      </template>
    </DataTable>

    <div v-if="showStudentModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Student Details</h5>
            <button
              type="button"
              class="btn-close"
              @click="showStudentModal = false"
            ></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="text-secondary">Name</label>
                <div class="fw-medium">{{ selectedStudent?.name }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Roll Number</label>
                <div class="fw-medium">{{ selectedStudent?.roll_no }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Department</label>
                <div class="fw-medium">{{ selectedStudent?.department }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">CGPA</label>
                <div class="fw-medium">{{ selectedStudent?.cgpa }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Email</label>
                <div class="fw-medium">{{ selectedStudent?.email }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Status</label>
                <div class="fw-medium">{{ selectedStudent?.status }}</div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showStudentModal = false">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showStudentModal" class="modal-backdrop fade show"></div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from "vue";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import StatCard from "@/components/shared/StatCard.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedStudent = ref(null);
const showStudentModal = ref(false);

const students = ref([
  {
    id: 1,
    name: "Rahul Sharma",
    roll_no: "24CS101",
    department: "CSE",
    cgpa: 8.9,
    email: "rahul@example.com",
    status: "Active",
  },
  {
    id: 2,
    name: "Priya Nair",
    roll_no: "24EC205",
    department: "ECE",
    cgpa: 8.4,
    email: "priya@example.com",
    status: "Inactive",
  },
  {
    id: 3,
    name: "Aman Verma",
    roll_no: "24ME112",
    department: "ME",
    cgpa: 7.9,
    email: "aman@example.com",
    status: "Blacklisted",
  },
  {
    id: 4,
    name: "Sneha Iyer",
    roll_no: "24CS143",
    department: "CSE",
    cgpa: 9.1,
    email: "sneha@example.com",
    status: "Active",
  },
]);

const headers = [
  { key: "name", label: "Name" },
  { key: "roll_no", label: "Roll No" },
  { key: "department", label: "Department" },
  { key: "cgpa", label: "CGPA" },
  { key: "status", label: "Status" },
  { key: "actions", label: "Actions" },
];

const filteredStudents = computed(() => {
  return students.value.filter((student) => {
    const query = searchQuery.value.toLowerCase();

    const matchesSearch =
      student.name.toLowerCase().includes(query) ||
      student.roll_no.toLowerCase().includes(query) ||
      student.department.toLowerCase().includes(query);

    const matchesStatus =
      !statusFilter.value ||
      student.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const totalStudents = computed(() => students.value.length);
const activeStudents = computed(
  () => students.value.filter((s) => s.status === "Active").length,
);
const inactiveStudents = computed(
  () => students.value.filter((s) => s.status === "Inactive").length,
);
const blacklistedStudents = computed(
  () => students.value.filter((s) => s.status === "Blacklisted").length,
);

const viewStudent = (student) => {
  selectedStudent.value = student;
  showStudentModal.value = true;
};

const deactivateStudent = (student) => {
  student.status = "Inactive";
};

const confirmDeactivate = (student) => {
  if (window.confirm(`Deactivate ${student.name}?`)) {
    deactivateStudent(student);
  }
};

const activateStudent = (student) => {
  student.status = "Active";
};

const blacklistStudent = (student) => {
  student.status = "Blacklisted";
};

const confirmBlacklist = (student) => {
  if (window.confirm(`Blacklist ${student.name}?`)) {
    blacklistStudent(student);
  }
};

const restoreStudent = (student) => {
  student.status = "Active";
};
</script>
