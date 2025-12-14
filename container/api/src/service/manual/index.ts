import packetService from '../restful/packet';
import domainService from '../restful/domain';

export class ManualService {
  async processManualPackets(data: any): Promise<any> {
    const targetUrl = Object.keys(data)[0];
    const reqResPackets = data[targetUrl];

    // Get current packet count before insertion
    const previousPacketCount = await packetService.countManual();

    // Insert packets with category = 1 (manual)
    const packetsToInsert = reqResPackets.map((packet: any) => ({
      category: 1,
      statusCode: packet.response?.status_code || 0,
      requestType: packet.request?.method || 'GET',
      requestJson: JSON.stringify(packet.request || {}),
      responseHeader: JSON.stringify(packet.response?.headers || {}),
      responseBody: packet.response?.body || '',
    }));

    await packetService.create(packetsToInsert);

    // Get packet indexes for the newly inserted packets
    const recentPacketCount = reqResPackets.length + previousPacketCount;
    const allManualIds = await packetService.getManualIds();
    const packetIndexes = allManualIds.slice(previousPacketCount, recentPacketCount);

    // Process and insert domains
    const domainsToInsert = reqResPackets.map((packet: any, index: number) => ({
      related_Packet: packetIndexes[index] || 0,
      URL: targetUrl,
      URI: packet.request?.url || '',
      action_URL: packet.request?.full_url || '',
      action_URL_Type: packet.request?.method || 'GET',
      params: this.extractParams(packet.request?.url || ''),
      comment: '',
      attackVector: 'Manual Analysis',
      impactRate: 0,
      description: 'Manually captured packet',
      Details: JSON.stringify({
        headers: packet.request?.headers || {},
        body: packet.request?.body || '',
      }),
    }));

    const insertedDomains = await domainService.create(domainsToInsert);

    return {
      success: true,
      message: 'Manual packets processed successfully',
      packetsInserted: reqResPackets.length,
      domainsInserted: Array.isArray(insertedDomains) ? insertedDomains.length : 1,
    };
  }

  private extractParams(url: string): string {
    try {
      const urlObj = new URL(url, 'http://dummy.com');
      const params: Record<string, string> = {};
      urlObj.searchParams.forEach((value, key) => {
        params[key] = value;
      });
      return JSON.stringify(params);
    } catch {
      return '{}';
    }
  }
}

export default new ManualService();
