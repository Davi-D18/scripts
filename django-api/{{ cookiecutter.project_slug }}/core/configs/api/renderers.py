from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # garantir dict para renderer_context
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")

        status_code = getattr(response, "status_code", None)

        # Quando não há conteúdo (204) retornar body vazio
        if status_code == 204:
            return b""

        success = True if (status_code is None or status_code < 400) else False
        
        if data is None:
            payload = {}
        elif isinstance(data, dict):
            payload = data.copy()
        else:
            payload = {"result": data}

        # Extrair e remover "detail" com segurança se existir
        detail = None
        if isinstance(payload, dict) and "detail" in payload:
            detail = payload.pop("detail")

        # Remover possível chave "success" que possa conflitar
        payload.pop("success", None)

        response_data = {"success": success, "data": payload}
        if detail is not None:
            response_data["detail"] = detail

        return super().render(response_data, accepted_media_type, renderer_context)

