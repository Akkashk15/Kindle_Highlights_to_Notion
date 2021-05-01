/**
 * @category Library Internal
 */
declare function post(url: string): {
    setHeader: (key: string, value: string) => any;
    sendAsJson: (body?: any) => Promise<any>;
};
export { post };
//# sourceMappingURL=httputil.d.ts.map