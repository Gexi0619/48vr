/**
 * 直播链接获取模块
 * 实现live_detail.py, live_sip.py, live_proc.py的功能
 */

class LiveFetcher {
  constructor() {
    this.apiUrl = "https://cvrapi.letinvr.com:10443/cmsClient/content/getContentDetail";
    this.headers = {
      "User-Agent": "UnityPlayer/2020.3.37f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)",
      "Accept": "*/*",
      "Accept-Encoding": "deflate, gzip",
      "Content-Type": "application/json",
      "columnTag": "20220506104225",
      "X-Unity-Version": "2020.3.37f1"
    };
    this.contentNumbers = ["42681814", "42268397"]; // SNH48 和 GNZ48
  }

  /**
   * 获取单个直播详情（对应live_detail.py功能）
   */
  async fetchLiveDetail(contentNumber) {
    const payload = {
      deviceType: 5,
      contentNumber: contentNumber,
      contentType: 4
    };

    try {
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(payload),
        mode: 'cors'
      });

      if (!response.ok) {
        throw new Error(`请求失败，状态码: ${response.status}`);
      }

      const respJson = await response.json();
      
      if (respJson.code !== 1000) {
        throw new Error(`接口返回错误: ${respJson.msg || '未知错误'}`);
      }

      return respJson.data;
    } catch (error) {
      console.error(`❌ contentNumber=${contentNumber} 获取失败:`, error);
      throw error;
    }
  }

  /**
   * 获取所有直播详情（对应live_detail.py + live_sip.py功能）
   */
  async fetchAllLiveDetails() {
    const allDetails = [];
    
    for (const contentNumber of this.contentNumbers) {
      try {
        const detail = await this.fetchLiveDetail(contentNumber);
        allDetails.push(detail);
        console.log(`✅ 成功获取 ${contentNumber} 的直播详情`);
      } catch (error) {
        console.error(`⚠️ 跳过 ${contentNumber}:`, error.message);
        // 继续处理其他的，不中断整个流程
      }
    }

    return allDetails;
  }

  /**
   * 简化直播数据（对应live_sip.py的simplify功能）
   */
  simplifyLiveData(data) {
    const simplified = [];
    
    for (const item of data) {
      const simple = {
        id: item.id,
        cnName: item.cnName,
        contentNumber: item.contentNumber,
        firstLetter: item.firstLetter,
        brief: item.brief,
        createTime: item.createTime,
        updateTime: item.updateTime,
        liveBroadcastSeats: []
      };

      for (const seat of (item.liveBroadcastSeats || [])) {
        // 跳过"免费机位"
        if (seat.name === "免费机位") {
          continue;
        }

        const simpleSeat = {
          id: seat.id,
          name: seat.name,
          liveBroadcastSeatAddressList: []
        };

        for (const addr of (seat.liveBroadcastSeatAddressList || [])) {
          simpleSeat.liveBroadcastSeatAddressList.push({
            address: addr.address
          });
        }

        // 只保留有地址的机位
        if (simpleSeat.liveBroadcastSeatAddressList.length > 0) {
          simple.liveBroadcastSeats.push(simpleSeat);
        }
      }

      simplified.push(simple);
    }

    return simplified;
  }

  /**
   * 处理直播数据用于页面展示（对应live_proc.py功能）
   */
  processLiveData(flatData) {
    const result = [];
    
    for (const item of flatData) {
      // 判断标题
      let cnName, firstLetter;
      if ((item.cnName || '').toUpperCase().includes('GNZ')) {
        cnName = 'GNZ48 剧场直播';
        firstLetter = 'G';
      } else {
        cnName = 'SNH48 剧场直播';
        firstLetter = 'S';
      }

      // 构造新结构
      const newItem = {
        id: item.id,
        cnName: cnName,
        date: '20301030',
        contentNumber: item.contentNumber || '',
        firstLetter: firstLetter,
        duration: item.updateTime ? `此直播链接发布时间: ${item.updateTime}` : '当公演开始后可以观看',
        brief: item.brief || '',
        createTime: item.createTime || '',
        updateTime: item.updateTime || '',
        liveBroadcastSeats: []
      };

      // 处理机位
      for (const seat of (item.liveBroadcastSeats || [])) {
        const seatObj = {
          name: seat.name || '',
          liveBroadcastSeatAddressList: (seat.liveBroadcastSeatAddressList || []).map(addr => ({
            address: addr.address || ''
          }))
        };
        newItem.liveBroadcastSeats.push(seatObj);
      }

      result.push(newItem);
    }

    return result;
  }

  /**
   * 完整的获取和处理流程
   */
  async fetchAndProcessLiveData() {
    try {
      console.log('🔄 开始获取直播数据...');
      
      // 1. 获取原始数据
      const rawData = await this.fetchAllLiveDetails();
      console.log('✅ 获取原始数据完成');
      
      // 2. 简化数据
      const simplifiedData = this.simplifyLiveData(rawData);
      console.log('✅ 数据简化完成');
      
      // 3. 处理数据用于展示
      const processedData = this.processLiveData(simplifiedData);
      console.log('✅ 数据处理完成');
      
      return processedData;
    } catch (error) {
      console.error('❌ 获取直播数据失败:', error);
      throw error;
    }
  }
}

/**
 * UI交互模块（简化版）
 */
class LiveUI {
  constructor() {
    this.liveFetcher = new LiveFetcher();
  }
}

// 导出供使用
window.LiveFetcher = LiveFetcher;
window.LiveUI = LiveUI;
