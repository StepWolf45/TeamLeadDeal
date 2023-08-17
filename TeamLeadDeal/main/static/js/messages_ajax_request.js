<script type="text/javascript">
        function load_data() {
            let xhr = new XMLHttpRequest();
            xhr.open(method="GET", url="/messages/data/"+{{recipient.pk}}, async=true);

            let data = "";

            xhr.onload = function() {
                let data = JSON.parse(xhr.response)["messages"];
                result.innerHTML = data;
            }

            let textMessage = resul



            xhr.send();
        }
        </script>