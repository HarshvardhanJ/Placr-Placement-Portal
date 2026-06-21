<template>
  <DashboardLayout>
    <PageHeader
      title="Students"
      subtitle="Manage student accounts, status, and records."
    >
      <template #actions>
        <button
          type="button"
          class="btn btn-primary d-inline-flex align-items-center gap-2"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
            <path d="M7 11l5 5l5 -5" />
            <path d="M12 4l0 12" />
          </svg>
          <span>Export</span>
        </button>
      </template>
    </PageHeader>

    <div class="row g-3 mb-4">
      <div
        v-for="stat in stats"
        :key="stat.title"
        class="col-12 col-sm-6 col-xl-3"
      >
        <StatCard :title="stat.title" :value="stat.value" />
      </div>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-center">
          <div class="col-lg-7">
            <div class="search-wrap">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="search-icon"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>

              <input
                v-model="searchQuery"
                type="text"
                class="form-control border-0 shadow-none"
                placeholder="Search by name, roll no, email, or contact..."
              />
            </div>
          </div>

          <div class="col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="active">Active</option>
              <option value="blacklisted">Blacklisted</option>
            </select>
          </div>

          <div class="col-lg-2">
            <button
              class="btn btn-outline-secondary w-100"
              type="button"
              @click="clearFilters"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <DataTable title="Students" :headers="headers" :rows="filteredStudents">
      <template #status="{ row }">
        <span class="badge rounded-pill" :class="statusBadgeClass(row.status)">
          {{ row.status }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="d-flex flex-wrap gap-2">
          <button
            class="btn btn-sm btn-outline-primary"
            @click="viewStudent(row)"
          >
            View
          </button>

          <button
            v-if="row.status !== 'Blacklisted'"
            class="btn btn-sm btn-outline-danger"
            @click="confirmBlacklist(row)"
          >
            Blacklist
          </button>
        </div>
      </template>
    </DataTable>

    <div v-if="showStudentModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header">
            <div>
              <h5 class="modal-title mb-1">Student Details</h5>
              <small class="text-secondary"
                >Profile and account information</small
              >
            </div>
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
                <label class="text-secondary">Contact</label>
                <div class="fw-medium">{{ selectedStudent?.phone_number }}</div>
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
import { ref, computed, onMounted } from "vue";
import api from "@/services/api";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import StatCard from "@/components/shared/StatCard.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedStudent = ref(null);
const showStudentModal = ref(false);

const students = ref([]);
const loading = ref(false);

const headers = [
  { key: "name", label: "Name" },
  { key: "roll_no", label: "Roll No" },
  { key: "department", label: "Department" },
  { key: "cgpa", label: "CGPA" },
  { key: "status", label: "Status" },
  { key: "actions", label: "Actions" },
];

const loadStudents = async () => {
  try {
    loading.value = true;

    const response = await api.get("/admin/students");

    students.value = response.data.map((student) => ({
      ...student,

      status: student.is_active ? "Active" : "Blacklisted",
    }));
  } catch (error) {
    console.error("Failed to load students:", error);
  } finally {
    loading.value = false;
  }
};

const stats = computed(() => [
  { title: "Total Students", value: students.value.length },
  {
    title: "Active",
    value: students.value.filter((s) => s.status === "Active").length,
  },
  {
    title: "Blacklisted",
    value: students.value.filter((s) => s.status === "Blacklisted").length,
  },
]);

const filteredStudents = computed(() => {
  return students.value.filter((student) => {
    const query = searchQuery.value.toLowerCase();

    const matchesSearch =
      student.name?.toLowerCase().includes(query) ||
      student.roll_no?.toLowerCase().includes(query) ||
      student.department?.toLowerCase().includes(query) ||
      student.email?.toLowerCase().includes(query) ||
      student.phone_number?.toLowerCase().includes(query);

    const matchesStatus =
      !statusFilter.value ||
      student.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

const statusBadgeClass = (status) => {
  switch (status) {
    case "Active":
      return "text-bg-success";
    case "Inactive":
      return "text-bg-warning";
    case "Blacklisted":
      return "text-bg-danger";
    default:
      return "text-bg-light";
  }
};

const viewStudent = (student) => {
  selectedStudent.value = student;
  showStudentModal.value = true;
};

const blacklistStudent = async (student) => {
  try {
    await api.put(`/admin/students/${student.student_id}/blacklist`);

    student.status = "Blacklisted";
    student.is_active = false;
  } catch (error) {
    console.error(error);
  }
};

const confirmBlacklist = (student) => {
  if (window.confirm(`Blacklist ${student.name}?`)) {
    blacklistStudent(student);
  }
};

onMounted(() => {
  loadStudents();
});
</script>

<style scoped>
.search-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 0.6rem 0.9rem;
}

.search-icon {
  color: #6b7280;
  flex-shrink: 0;
}
</style>
