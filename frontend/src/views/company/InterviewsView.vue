<template>
  <CompanyLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Interviews"
      subtitle="Track upcoming and past interviews across all drives."
    />

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

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
          <div class="col-lg-5">
            <div class="tab-pills">
              <button
                v-for="tab in tabs"
                :key="tab.key"
                type="button"
                class="tab-pill"
                :class="{ active: activeTab === tab.key }"
                @click="activeTab = tab.key"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>

          <div class="col-lg-5">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search by student or role..."
            />
          </div>

          <div class="col-lg-2">
            <button
              class="btn btn-outline-secondary w-100"
              type="button"
              @click="searchQuery = ''"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="card shadow-sm p-5 text-center">
      Loading interviews...
    </div>

    <DataTable
      v-else
      title="Interviews"
      :headers="headers"
      :rows="filteredInterviews"
    >
      <template #student="{ row }">
        <div class="fw-semibold">{{ row.student_name }}</div>
        <small class="text-muted">{{ row.roll_no }}</small>
      </template>

      <template #interview_date="{ row }">
        {{ formatDateTime(row.interview_date) }}
      </template>

      <template #interview_type="{ row }">
        <span class="badge rounded-pill bg-light text-dark border">
          {{ row.interview_type === "inPerson" ? "In Person" : "Online" }}
        </span>
      </template>

      <template #status="{ row }">
        <span class="badge rounded-pill" :class="statusBadgeClass(row.status)">
          {{ formatStatus(row.status) }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="d-flex flex-wrap gap-2">
          <button
            class="btn btn-sm btn-outline-primary"
            @click="openReschedule(row)"
          >
            Reschedule
          </button>
          <button
            v-if="row.status === 'shortlisted'"
            class="btn btn-sm btn-success"
            @click="confirmUpdate(row, 'selected')"
          >
            Select
          </button>
          <button
            v-if="row.status === 'shortlisted'"
            class="btn btn-sm btn-outline-danger"
            @click="confirmUpdate(row, 'rejected')"
          >
            Reject
          </button>
        </div>
      </template>
    </DataTable>

    <ScheduleInterviewModal
      :show="showScheduleModal"
      :application="selectedInterview"
      @close="showScheduleModal = false"
      @saved="onSaved"
    />
  </CompanyLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import api from "@/services/api";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import ScheduleInterviewModal from "@/components/company/ScheduleInterviewModal.vue";

const searchQuery = ref("");
const activeTab = ref("upcoming");
const loading = ref(false);
const error = ref("");
const interviews = ref([]);

const showScheduleModal = ref(false);
const selectedInterview = ref(null);

const tabs = [
  { key: "upcoming", label: "Upcoming" },
  { key: "past", label: "Past" },
  { key: "all", label: "All" },
];

const headers = [
  { key: "student", label: "Student" },
  { key: "job_title", label: "Role" },
  { key: "interview_date", label: "Date & Time" },
  { key: "interview_type", label: "Mode" },
  { key: "status", label: "Status" },
  { key: "actions", label: "Actions" },
];

const loadInterviews = async () => {
  loading.value = true;
  error.value = "";
  try {
    const { data } = await api.get("/company/interviews");
    interviews.value = data.interviews;
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load interviews";
  } finally {
    loading.value = false;
  }
};

const stats = computed(() => [
  { title: "Total Interviews", value: interviews.value.length },
  {
    title: "Upcoming",
    value: interviews.value.filter((i) => i.is_upcoming).length,
  },
  {
    title: "Online",
    value: interviews.value.filter((i) => i.interview_type === "online").length,
  },
  {
    title: "In Person",
    value: interviews.value.filter((i) => i.interview_type === "inPerson")
      .length,
  },
]);

const filteredInterviews = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return interviews.value.filter((interview) => {
    const matchesTab =
      activeTab.value === "all" ||
      (activeTab.value === "upcoming" && interview.is_upcoming) ||
      (activeTab.value === "past" && !interview.is_upcoming);

    const matchesSearch =
      !query ||
      interview.student_name?.toLowerCase().includes(query) ||
      interview.job_title?.toLowerCase().includes(query);

    return matchesTab && matchesSearch;
  });
});

const formatDateTime = (value) => {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
};

const statusBadgeClass = (status) => {
  switch (status) {
    case "shortlisted":
      return "text-bg-warning";
    case "selected":
      return "text-bg-success";
    case "rejected":
      return "text-bg-danger";
    default:
      return "text-bg-light";
  }
};

const formatStatus = (status = "") =>
  status ? status.charAt(0).toUpperCase() + status.slice(1) : "";

const openReschedule = (interview) => {
  selectedInterview.value = interview;
  showScheduleModal.value = true;
};

const onSaved = () => {
  showScheduleModal.value = false;
  loadInterviews();
};

const confirmUpdate = (interview, status) => {
  const verb = status === "selected" ? "select" : "reject";
  if (window.confirm(`Mark ${interview.student_name} as ${verb}ed?`)) {
    updateStatus(interview, status);
  }
};

const updateStatus = async (interview, status) => {
  try {
    await api.put(
      `/company/drives/${interview.drive_id}/applications/${interview.application_id}`,
      {
        status,
      },
    );
    loadInterviews();
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to update application";
  }
};

onMounted(() => {
  loadInterviews();
});
</script>

<style scoped>
.tab-pills {
  display: inline-flex;
  gap: 0.25rem;
  background: #eef1f6;
  padding: 0.25rem;
  border-radius: 10px;
}

.tab-pill {
  border: 0;
  background: transparent;
  padding: 0.4rem 0.9rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  color: #5f6b7a;
}

.tab-pill.active {
  background: #ffffff;
  color: #0d6efd;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08);
}
</style>
