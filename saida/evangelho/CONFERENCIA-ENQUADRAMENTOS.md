# Conferência dos cinco enquadramentos

Baseline: main em e32d623586376ce93a91dd9be0e7343a3350fb26.

Conferência aprovada.

Somente os focos e zooms das cinco datas abaixo mudaram no YAML. Todos os demais bytes do YAML, inclusive comentários e as outras dez datas, foram preservados.

| Data | Foco | Zoom |
| --- | --- | --- |
| 2026-11-30 | 10% 50% | 1 |
| 2026-12-05 | 25% 50% | 1.1 |
| 2026-12-07 | 50% 20% | 1.04 |
| 2026-12-10 | 50% 98% | 1 |
| 2026-12-12 | 50% 3% | 1.6 |

282 saídas protegidas continuam idênticas byte a byte. As dez pastas do Evangelho não selecionadas continuam integralmente idênticas; seus PNGs foram comparados também pixel a pixel. As demais séries, as obras originais, o código, os testes e o kit não mudaram.

Nas cinco datas selecionadas, os cards textuais mantêm os mesmos PNGs byte a byte e os mesmos pixels. Nas capas, cada pixel fora do clip real da obra em arco é idêntico. A máscara foi obtida no próprio Chromium pela diferença entre uma imagem preta e uma branca no DOM/CSS inalterado de cada capa, mantendo foco, zoom e transformações; ela inclui exatamente o antialias da curva.
A máscara registra 5 ocorrências de pixels alterados de antialias da curva que uma máscara de círculo analítico não cobria; os pixels estão dentro do clip real do Chromium. Coordenadas e diferenças RGB estão na evidência JSON. Nenhuma tolerância de cor ou dilatação arbitrária foi usada.
Os textos e caixas medidos nas quinze datas mantêm as mesmas linhas, estilos, posições e distâncias. A tabela do lote não mudou. Os recortes foram reconstruídos pelo foco e zoom aprovados; nenhuma margem uniforme é visível.

Os quinze PDFs mantêm 48 páginas no total, na ordem dos cards, com texto igual ao YAML, espaços entre palavras preservados e quatro variantes de fontes embutidas. PyMuPDF e pdftotext confirmaram o texto. Nos cinco PDFs regenerados, textos, glifos, posições e tabelas das fontes permanecem iguais ao baseline; as páginas de texto também têm raster idêntico.
A prancha com quinze datas foi reconstruída a partir dos PNGs finais. A prancha de cores continua idêntica byte a byte e pixel a pixel. A verificação agregada cobre quinze datas e 65 PNGs.

A inspeção visual foi atualizada nas cinco notas. Em 12/12, os dois santos da frente e as pontas antes visíveis ficaram fora do arco; Maria e Isabel conservam rostos, halos e mãos, com saias inferiores e pés ainda fora do recorte.
As outras oito notas do lote foram preservadas, incluindo a exclusão dos elementos indesejados em 9/12.

177 testes passaram.

Pendente: conferir a importação dos cinco PDFs regenerados no Canva. As limitações de enquadramento restantes estão registradas no relatório e nas notas das obras.

Evidência detalhada: [conferencia-enquadramentos.json](conferencia-enquadramentos.json).
