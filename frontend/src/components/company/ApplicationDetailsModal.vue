<template>
  <div v-if="show" class="modal d-block" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <div>
            <h5 class="modal-title mb-1">Application Details</h5>
            <small class="text-secondary">{{ application?.job_title }}</small>
          </div>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>

          <div class="row g-3">
            <div class="col-md-6">
              <label class="text-secondary">Student Name</label>
              <div class="fw-medium">{{ application?.student_name }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Roll No</label>
              <div class="fw-medium">{{ application?.roll_no }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Department</label>
              <div class="fw-medium">{{ application?.department || "—" }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">CGPA</label>
              <div class="fw-medium">{{ application?.cgpa ?? "—" }}</div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Status</label>
              <div>
                <span class="badge rounded-pill" :class="statusBadgeClass(application?.status)">
                  {{ formatStatus(application?.status) }}
                </span>
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Applied On</label>
              <div class="fw-medium">{{ application?.application_date }}</div>
            </div>

            <div v-if="application?.interview_date" class="col-md-6">
              <label class="text-secondary">Interview</label>
              <div class="fw-medium">
                {{ application.interview_date }} · {{ interviewTypeLabel }}
              </div>
            </div>

            <div v-if="application?.remarks" class="col-12">
              <label class="text-secondary">Remarks</label>
              <div class="fw-medium">{{ application.remarks }}</div>
            </div>

            <div class="col-12">
              <label class="text-secondary">Resume</label>
              <div>
                <button
                  v-if="application?.resume_uploaded"
                  type="button"
                  class="btn btn-outline-primary btn-sm"
                  @click="viewResume"
                  :disabled="loadingResume"
                >
                  <i class="ti ti-file-text me-1"></i>
                  {{ loadingResume ? "Opening..." : "View Resume" }}
                </button>
                <span v-else class="text-muted">Not uploaded</span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer flex-wrap gap-2">
          <template v-if="application?.status === 'applied'">
            <button class="btn btn-outline-danger" @click="reject">Reject</button>
            <button class="btn btn-primary" @click="$emit('schedule', application)">
              Shortlist &amp; Schedule
            </button>
          </template>

          <template v-else-if="application?.status === 'shortlisted'">
            <button class="btn btn-outline-danger" @click="reject">Reject</button>
            <button class="btn btn-outline-primary" @click="$emit('schedule', application)">
              Reschedule
            </button>
            <button class="btn btn-success" @click="select">Mark Selected</button>
          </template>

          <button class="btn btn-secondary" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="show" class="modal-backdrop fade show"></div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import api from "@/services/api";
import { openApplicantResume } from "@/utils/resume";

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  application: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "saved", "schedule"]);

const error = ref("");
const loadingResume = ref(false);
const saving = ref(false);

watch(
  () => props.show,
  (value) => {
    if (value) error.value = "";
  },
);

const interviewTypeLabel = computed(() => {
  if (props.application?.interview_type === "inPerson") return "In Person";
  if (props.application?.interview_type === "online") return "Online";
  return "";
});

const statusBadgeClass = (status) => {
  switch (status) {
    case "applied":
      return "text-bg-secondary";
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

const viewResume = async () => {
  loadingResume.value = true;
  try {
    await openApplicantResume(props.application.application_id);
  } catch (err) {
    error.value = "Failed to open resume";
  } finally {
    loadingResume.value = false;
  }
};

const updateStatus = async (status, extra = {}) => {
  if (!props.application) return;
  error.value = "";
  saving.value = true;
  try {
    await api.put(
      `/company/drives/${props.application.drive_id}/applications/${props.application.application_id}`,
      { status, ...extra },
    );
    emit("saved");
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to update application";
  } finally {
    saving.value = false;
  }
};

const reject = () => {
  if (window.confirm(`Reject ${props.application?.student_name}'s application?`)) {
    updateStatus("rejected");
  }
};

const select = () => {
  if (window.confirm(`Mark ${props.application?.student_name} as selected?`)) {
    updateStatus("selected");
  }
};
</script>
