<template>
  <div v-if="show" class="modal d-block" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <div>
            <h5 class="modal-title mb-1">{{ isReschedule ? "Reschedule Interview" : "Shortlist & Schedule Interview" }}</h5>
            <small class="text-secondary">{{ application?.student_name }} — {{ application?.job_title }}</small>
          </div>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <div class="mb-3">
              <label class="form-label">Interview Date &amp; Time <span class="text-danger">*</span></label>
              <input
                v-model="interviewDate"
                type="datetime-local"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Interview Type <span class="text-danger">*</span></label>
              <select v-model="interviewType" class="form-select" required>
                <option value="online">Online</option>
                <option value="inPerson">In Person</option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label">Remarks (optional)</label>
              <textarea v-model="remarks" class="form-control" rows="2"></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? "Saving..." : isReschedule ? "Update Interview" : "Shortlist Candidate" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-if="show" class="modal-backdrop fade show"></div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import api from "@/services/api";

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  // { application_id, drive_id, student_name, job_title, interview_date?, interview_type?, remarks? }
  application: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "saved"]);

const interviewDate = ref("");
const interviewType = ref("online");
const remarks = ref("");
const saving = ref(false);
const error = ref("");

const isReschedule = computed(() => Boolean(props.application?.interview_date));

watch(
  () => props.show,
  (value) => {
    if (!value) return;
    error.value = "";
    interviewType.value = props.application?.interview_type || "online";
    remarks.value = props.application?.remarks || "";
    interviewDate.value = props.application?.interview_date
      ? props.application.interview_date.slice(0, 16)
      : "";
  },
);

const handleSubmit = async () => {
  if (!props.application) return;

  error.value = "";
  saving.value = true;

  try {
    await api.put(
      `/company/drives/${props.application.drive_id}/applications/${props.application.application_id}`,
      {
        status: "shortlisted",
        interview_date: interviewDate.value,
        interview_type: interviewType.value,
        remarks: remarks.value || null,
      },
    );
    emit("saved");
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to schedule interview";
  } finally {
    saving.value = false;
  }
};
</script>
