<template>
  <div class="card shadow-sm border-0 h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start gap-2 mb-3">
        <div>
          <h6 class="mb-1 fw-semibold">Recent Activity</h6>
          <small class="text-muted">Applications and status updates</small>
        </div>
        <RouterLink to="/student/applications" class="btn btn-link btn-sm text-decoration-none">
          View All
        </RouterLink>
      </div>

      <div class="activity-list">
        <div
          v-for="item in items"
          :key="item.key"
          class="activity-item"
        >
          <div class="activity-dot" :class="item.dotClass"></div>
          <div class="flex-grow-1 min-w-0">
            <div class="fw-semibold">{{ item.title }}</div>
            <small class="text-muted">{{ item.subtitle }}</small>
          </div>
          <small class="text-muted text-nowrap">{{ item.time }}</small>
        </div>
      </div>

      <div v-if="!items.length" class="mt-3">
        <StudentEmptyState
          icon="ti-list-details-off"
          title="No activity yet"
          subtitle="Applications and interview updates will appear here."
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import StudentEmptyState from "./StudentEmptyState.vue";

const props = defineProps({
  applications: {
    type: Array,
    default: () => [],
  },
  shortlisted: {
    type: Array,
    default: () => [],
  },
  selected: {
    type: Array,
    default: () => [],
  },
});

const formatRelative = (value) => {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  const diff = Math.max(0, Date.now() - date.getTime());
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
};

const items = computed(() => {
  const list = [];

  props.applications.slice(0, 2).forEach((app) => {
    list.push({
      key: `app-${app.application_id || app.drive?.drive_id}`,
      title: "Application submitted",
      subtitle: `${app.drive?.company?.name || app.drive?.company_name || "Company"} · ${app.drive?.job_title || app.job_title || "Role"}`,
      time: formatRelative(app.application_date) || "Recently",
      dotClass: "dot-neutral",
    });
  });

  props.shortlisted.slice(0, 1).forEach((app) => {
    list.push({
      key: `short-${app.application_id}`,
      title: "Shortlisted",
      subtitle: `${app.drive?.company?.name || app.drive?.company_name || "Company"} · Interview stage`,
      time: formatRelative(app.interview_date) || "Soon",
      dotClass: "dot-warning",
    });
  });

  props.selected.slice(0, 1).forEach((app) => {
    list.push({
      key: `sel-${app.application_id}`,
      title: "Selected",
      subtitle: `${app.drive?.company?.name || app.drive?.company_name || "Company"} · Offer received`,
      time: "Placed",
      dotClass: "dot-success",
    });
  });

  return list.slice(0, 4);
});
</script>

<style scoped>
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.8rem 0.9rem;
  border-radius: 14px;
  border: 1px solid #e9ecef;
  background: #fff;
}

.activity-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 0.4rem;
  flex-shrink: 0;
}

.dot-neutral {
  background: #94a3b8;
}

.dot-warning {
  background: #f59e0b;
}

.dot-success {
  background: #22c55e;
}
</style>
