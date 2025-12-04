function openDeleteModal(id, nome) {
  if (!window.modalEnabled) return;

  document.getElementById("modalNome").textContent = nome;

  const base = window.location.pathname.split("/")[1];
  // “estoque” in your case

  const form = document.getElementById("modalForm");
  form.action = `/${base}/excluir/${id}/`;

  document.getElementById("deleteModal").style.display = "block";
}

function closeModal() {
  document.getElementById("deleteModal").style.display = "none";
}
