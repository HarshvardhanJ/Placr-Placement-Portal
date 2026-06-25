import api from "@/services/api";

export async function openApplicantResume(applicationId) {
  const newTab = window.open("", "_blank");

  try {
    const response = await api.get(
      `/company/applications/${applicationId}/resume`,
      {
        responseType: "blob",
      },
    );

    const blobUrl = URL.createObjectURL(response.data);

    if (newTab) {
      newTab.location = blobUrl;
    } else {
      window.open(blobUrl, "_blank");
    }
  } catch (error) {
    if (newTab) newTab.close();
    throw error;
  }
}
