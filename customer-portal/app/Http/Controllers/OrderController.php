<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class OrderController extends Controller
{
    public function store(Request $request)
    {
        // 1. Validação rápida no PHP (BFF)
        $data = $request->validate([
            'customerEmail' => 'required|email',
            'amount' => 'required|numeric|min:1'
        ]);

        try {
            // 2. Chamada para o Microserviço Java usando a URL da rede Docker
            // O Java espera 'totalAmount', então mapeamos aqui
            $response = Http::post(env('ORDER_SERVICE_URL') . '/orders', [
                'customerEmail' => $data['customerEmail'],
                'amount' => $data['amount'] 
            ]);

            if ($response->successful()) {
                return back()->with('success', 'Pedido #' . $response->json()['id'] . ' criado com sucesso via Java!');
            }

            return back()->with('error', 'Erro no Serviço de Ordens: ' . $response->status());
        } catch (\Exception $e) {
            Log::error("Falha ao conectar no Java: " . $e->getMessage());
            return back()->with('error', 'Não foi possível conectar ao serviço Java.');
        }
    }
}