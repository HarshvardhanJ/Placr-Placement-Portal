<template>
  <div v-if="show" class="modal d-block" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <div>
            <h5 class="modal-title mb-1">{{ modalTitle }}</h5>
            <small class="text-secondary">{{ modalSubtitle }}</small>
          </div>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <div class="row g-3">
              <div class="col-md-8">
                <label class="form-label">Job Title <span v-if="!readOnly" class="text-danger">*</span></label>
                <input
                  v-model="form.job_title"
                  type="text"
                  class="form-control"
                  :readonly="readOnly"
                  required
                  placeholder="e.g. Software Engineer"
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Location</label>
                <input
                  v-model="form.job_location"
                  type="text"
                  class="form-control"
                  :readonly="readOnly"
                  placeholder="e.g. Bengaluru"
                />
              </div>

              <div class="col-12">
                <label class="form-label">Job Description</label>
                <textarea
                  v-model="form.job_description"
                  class="form-control"
                  rows="3"
                  :readonly="readOnly"
                  placeholder="Role responsibilities, expectations..."
                ></textarea>
              </div>

              <div class="col-md-4">
                <label class="form-label">Application Deadline <span v-if="!readOnly" class="text-danger">*</span></label>
                <input
                  v-model="form.application_deadline"
                  type="date"
                  class="form-control"
                  :readonly="readOnly"
                  required
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Eligible Branch</label>
                <input
                  v-model="form.eligible_branch"
                  type="text"
                  class="form-control"
                  :readonly="readOnly"
                  placeholder="e.g. CSE, ECE"
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Eligible Year</label>
                <input
                  v-model.number="form.year"
                  type="number"
                  min="1"
                  max="6"
                  class="form-control"
                  :readonly="readOnly"
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Minimum CGPA</label>
                <input
                  v-model.number="form.min_cgpa"
                  type="number"
                  min="0"
                  max="10"
                  step="0.1"
                  class="form-control"
                  :readonly="readOnly"
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Number of Openings</label>
                <input
                  v-model.number="form.no_openings"
                  type="number"
                  min="1"
                  class="form-control"
                  :readonly="readOnly"
                />
              </div>

              <div class="col-md-4">
                <label class="form-label">Salary (CTC, per annum)</label>
                <input
                  v-model.number="form.salary"
                  type="number"
                  min="0"
                  class="form-control"
                  :readonly="readOnly"
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Required Skills</label>
                <textarea
                  v-model="form.required_skills"
                  class="form-control"
                  rows="2"
                  :readonly="readOnly"
                  placeholder="e.g. Python, SQL, REST APIs"
                ></textarea>
              </div>

              <div class="col-md-6">
                <label class="form-label">Experience Required</label>
                <input
                  v-model="form.experience_required"
                  type="text"
                  class="form-control"
                  :readonly="readOnly"
                  placeholder="e.g. 0-1 years"
                />
              </div>

              <div class="col-12">
                <label class="form-label">Benefits</label>
                <textarea
                  v-model="form.benefits"
                  class="form-control"
                  rows="2"
                  :readonly="readOnly"
                  placeholder="e.g. Health insurance, relocation support"
                ></textarea>
              </div>

              <div v-if="drive" class="col-12">
                <label class="text-secondary">Status</label>
                <div>
                  <span class="badge rounded-pill" :class="statusBadgeClass(drive.approval_status)">
                    {{ formatStatus(drive.approval_status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">
              {{ readOnly ? "Close" : "Cancel" }}
            </button>
            <button v-if="!readOnly" type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? "Saving..." : drive ? "Save Changes" : "Create Drive" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-if="show" class="modal-backdrop fade show"></div>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import api from "@/services/api";

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  drive: {
    type: Object,
    default: null,
  },
  // Allows opening an existing (pending) drive directly in edit mode
  startInEditMode: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close", "saved"]);

const blankForm = () => ({
  job_title: "",
  job_location: "",
  job_description: "",
  application_deadline: "",
  eligible_branch: "",
  min_cgpa: null,
  year: null,
  no_openings: null,
  salary: null,
  required_skills: "",
  experience_required: "",
  benefits: "",
});

const form = reactive(blankForm());
const saving = ref(false);
const error = ref("");
const editing = ref(false);

const readOnly = computed(() => {
  if (!props.drive) return false; // creating
  return !editing.value;
});

const modalTitle = computed(() => {
  if (!props.drive) return "Create Job Drive";
  return editing.value ? "Edit Job Drive" : "Drive Details";
});

const modalSubtitle = computed(() => {
  if (!props.drive) return "Post a new placement drive for admin approval.";
  return editing.value
    ? "Only pending drives can be edited."
    : "Placement drive overview.";
});

const populateForm = () => {
  Object.assign(form, blankForm());
  error.value = "";

  if (props.drive) {
    form.job_title = props.drive.job_title || "";
    form.job_location = props.drive.job_location || "";
    form.job_description = props.drive.job_description || "";
    form.application_deadline = (props.drive.application_deadline || "").slice(0, 10);
    form.eligible_branch = props.drive.eligible_branch || "";
    form.min_cgpa = props.drive.min_cgpa ?? null;
    form.year = props.drive.year ?? null;
    form.no_openings = props.drive.no_openings ?? null;
    form.salary = props.drive.salary ?? null;
    form.required_skills = props.drive.required_skills || "";
    form.experience_required = props.drive.experience_required || "";
    form.benefits = props.drive.benefits || "";
    editing.value = Boolean(props.startInEditMode);
  } else {
    editing.value = true;
  }
};

watch(() => props.show, (value) => {
  if (value) populateForm();
});

const statusBadgeClass = (status) => {
  switch (status) {
    case "approved":
      return "text-bg-success";
    case "pending":
      return "text-bg-warning";
    case "closed":
      return "text-bg-secondary";
    case "rejected":
      return "text-bg-danger";
    default:
      return "text-bg-light";
  }
};

const formatStatus = (status = "") =>
  status.charAt(0).toUpperCase() + status.slice(1);

const handleSubmit = async () => {
  error.value = "";
  saving.value = true;

  const payload = {
    job_title: form.job_title,
    job_location: form.job_location || null,
    job_description: form.job_description || null,
    application_deadline: `${form.application_deadline}T23:59:59`,
    eligible_branch: form.eligible_branch || null,
    min_cgpa: form.min_cgpa,
    year: form.year,
    no_openings: form.no_openings,
    salary: form.salary,
    required_skills: form.required_skills || null,
    experience_required: form.experience_required || null,
    benefits: form.benefits || null,
  };

  try {
    if (props.drive) {
      await api.put(`/company/drives/${props.drive.drive_id}`, payload);
    } else {
      await api.post("/company/drives", payload);
    }
    emit("saved");
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to save drive";
  } finally {
    saving.value = false;
  }
};
</script>
