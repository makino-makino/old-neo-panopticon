//
//  ViewController.swift
//  neopano
//
//  Created by shunta nakajima on 2019/11/25.
//  Copyright © 2019 Shunta Nakajima. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet var webView: UIWebView!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        let url = URL(string : "http://192.168.43.151:3001")
        let urlRequest = URLRequest.init(url: url!)
        self.webView.loadRequest(urlRequest)
        webView.scrollView.bounces = false
    }


}

